#!/usr/bin/env python
import os
import SocketServer
import threading
import random
import time

from Crypto.Cipher.AES import AESCipher

key = 'XXXXXXXXXXXXXXXX' # obviously, this is not the real key.
secret_data = 'This is not the real secret data'

class threadedserver(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

def pkcs7_pad(s):
  l = len(s)
  needed = 16 - (l % 16)
  return s + (chr(needed) * needed)

def pkcs7_unpad(s):
  # this is not actually used, but we wanted to put it in so you could see how to implement it.
  assert len(s) % 16 == 0
  assert len(s) >= 16
  last_char = s[-1]
  count = ord(last_char)
  assert 0 < count <= 16
  assert s[-count:] == last_char * count
  return s[:-count]

def oracle(s):
  # so, this is simulated. In reality we'd have to run javascript on a target web browser
  # and capture the traffic. That's pretty hard to do in a way that scales, though, so we
  # simulate it instead.
  # This uses ECB mode.
  return AESCipher(key).encrypt(pkcs7_pad('GET /' + s.decode('hex') + secret_data))

class incoming(SocketServer.StreamRequestHandler):
  def handle(self):
    self.request.send("Please send the path you'd like them to visit, hex-encoded.\n")
    data = self.request.recv(4096).strip('\n')
    self.request.send(oracle(data).encode('hex') + '\n')
    self.request.close()

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
  HOST = '0.0.0.0'
  PORT = 65414
  SocketServer.TCPServer.allow_reuse_address = True
  server = ReusableTCPServer((HOST, PORT), incoming)
  server.serve_forever()
