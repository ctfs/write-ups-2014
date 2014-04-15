#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import time
import random
import ctypes

from hashlib import sha1
from random import randint
from SocketServer import *


N = 0xcec903bcc749d3fdcf6a52d6ac3da6d9c9d70695e0860c92474edbe501620e1228bac1fdcd85bcdd24d7d185998a101313ab63a51d08bcada29701bea5ffd44f1a3e9bf56e211523d145e9054936fab8fee0e3a2b93c19f49bceb80aeda1e3cb564a917e7fa9bfc4a21ccb0f61f6bc7cafdce354ad6ef77a5c5f100cfa307381L
NCHAL = 313333333333333333333333333333333333336
E = 31337
D = int(open("secret").read().strip())
PASSWORD = open("password").read()

EXECMOD = ctypes.cdll.LoadLibrary("./exec.so")


class ExecServer(ForkingMixIn, TCPServer):
    pass


class ExecHandler(BaseRequestHandler):
    def handle(self):
        random.seed(str(time.time) + str(os.getpid()))

        client = self.request
        client.settimeout(5.0)

        client.sendall("Remote Shellcoding Appliance\n")
        client.sendall("1. Sign code\n")
        client.sendall("2. Execute code\n")
        client.sendall("3. Exit\n")
        client.sendall("4. Debug\n")

        choice = client.recv(2).strip()
        {
            "1": self.cmd_sign,
            "2": self.cmd_execute,
            "4": self.cmd_debug,
        }.get(choice, lambda *args: 1)(client)

        client.sendall("let pwn god be with you\n")

    def cmd_sign(self, client):
        client.sendall("Enter shellcode + sha1 in hex:\n")

        shellcode = self.read_line(client).strip().decode("hex")
        shellcode = s2n(shellcode)

        sign = pow(shellcode, D, N)

        rand = randint(1, NCHAL - 1)
        challenge = (pow(31337 + 31336 * (rand + sign), 31337, NCHAL) + sign) % NCHAL
        challenge = hex(challenge)[2:].rstrip("L")

        client.send("Challenge is %s. Your response:\n" % challenge)
        password = client.recv(32).strip()
        if sha1(challenge + password).digest() != sha1(challenge + PASSWORD).digest():
            client.sendall("denied\n")
        else:
            client.sendall(n2s(sign).encode("hex") + "\n")
        return

    def cmd_execute(self, client):
        client.sendall("Enter signed shellcode in hex:\n")

        sign = self.read_line(client).strip().decode("hex")
        sign = s2n(sign)
        signed_shellcode = pow(sign, E, N)
        signed_shellcode = n2s(signed_shellcode).rjust(128, "\x00")

        shellcode = signed_shellcode[1:-20]
        hash = signed_shellcode[-20:]

        if sha1(shellcode).digest() != hash:
            client.sendall("Hacker detected\n")
            return

        EXECMOD.run(shellcode, len(shellcode))

    def cmd_debug(self, client):
        client.sendall("You want to debug me??? lol\n")

    def read_line(self, client, max_read=4096):
        buf = ""
        while len(buf) < max_read and "\n" not in buf:
            s = client.recv(1)
            if not s:
                break
            buf += s
        return buf


def s2n(s):
    if not len(s):
        return 0
    return int(s.encode("hex"), 16)


def n2s(n):
    s = hex(n)[2:].rstrip("L")
    if len(s) % 2 != 0:
        s = "0" + s
    return s.decode("hex")


if __name__ == "__main__":
    [[[[[#
     [[[[[#
      [[[[[#
       [[[[[#
        [[[[[#
         setattr(ExecServer,
                            "allow_reuse_address",
                                                  True)

         or

         setattr(
                 ExecServer,
                            "server",
                                     ExecServer(("0.0.0.0", 3123), ExecHandler))

         or

         getattr(ExecServer
                           .server,
                                   "serve_forever")()

        ]]]]]#
       ]]]]]#
      ]]]]]#
     ]]]]]#
    ]]]]]#
