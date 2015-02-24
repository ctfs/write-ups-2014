#!/usr/bin/python

""" Police Directory Service v1.2"""

import socketserver
import sys
import struct
import random
import json

from os import urandom

HOST = 'localhost'
PORT = 21212

def xor(buf, key):
    """ Repeated key xor """

    encrypted = []
    for i, cr in enumerate(buf):
        k = key[i % len(key)]
        encrypted += [cr ^ k]
    return bytes(encrypted)

def secure_pad(buf):
    """ Ensure message is padded to block size. """
    key = urandom(5)
    buf = bytes([0x13, 0x33, 0x7B, 0xEE, 0xF0]) + buf
    buf = buf + urandom(16 - len(buf) % 16)
    enc = xor(buf, key)
    return enc

def remove_pad(buf):
    """ Removes the secure padding from the msg. """
    if len(buf) > 0 and len(buf) % 16 == 0:
        encrypted_key = buf[:5]
        key = xor(encrypted_key, bytes([0x13, 0x33, 0x7B, 0xEE, 0xF0]))
        dec = xor(buf, key)
        return dec[5:20]

def generate_cookie():
    """ Generates random transaction cookie. """
    cookie = random.randrange(1, 1e8)
    return cookie


class TCPConnectionHandler(socketserver.BaseRequestHandler):
    """ TCP Server """

    OFFICERS = json.loads(open("data.json", "r").read())
    client_information = {}

    def get_officer_data(self, entry):
        """ Retrieve binary format of officer. """

        if 0 <= entry and entry < len(self.OFFICERS):
            return json.dumps(self.OFFICERS[entry]).encode("utf-8")
        return None

    def secure_send(self, msg):
        """ Sends msg back to the client securely. """

        cookie = generate_cookie()
        data = struct.pack("!B2L128s", 0xFF, cookie, len(msg), msg)
        encrypted = secure_pad(data)
        self.request.sendall(encrypted)
        return cookie

    def handle(self):
        """ Handle client session"""
        running = True
        cookie = None
        access = False

        while running:
            data = self.request.recv(1024)
            if len(data) > 0:
                if not access:
                    try:
                        code = struct.unpack("!i", data)[0]
                        if code == 0xAA:
                            cookie = self.secure_send(b"WELCOME TO THE POLICE RECORDS DIRECTORY")
                            access = True
                        else:
                            raise Exception
                    except Exception as e:
                        raise e
                        self.request.sendall(b"ACCESS CODE DENIED")
                        running = False
                else:
                    if len(data) % 16 == 0:
                        decrypted = remove_pad(data)
                        try:
                            magic, user_cookie, badge, cmd, entry = \
                                    struct.unpack("!B2LHL", decrypted)
                            if magic != 0xFF or user_cookie != cookie:
                                self.request.sendall(b"INSECURE REQUEST")
                                running = False
                            else:
                                if cmd == 1:
                                    officer = self.get_officer_data(entry)
                                    if officer:
                                        cookie = self.secure_send(officer)
                                    else:
                                        cookie = self.secure_send(b"INVALID ENTRY -- OFFICER DOES NOT EXIST")
                                else:
                                    cookie = self.secure_send(b"INVALID COMMAND")
                        except Exception as e:
                            raise e
                            self.request.sendall(b"MALFORMED REQUEST")
                            running = False
            else:
                running = False
        self.request.close()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = Server((HOST, PORT), TCPConnectionHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
