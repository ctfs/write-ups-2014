#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import random

from SocketServer import *


FLAG = int(open("flag").read().strip().encode("hex"), 16)
assert 1 << 256 < FLAG < 1 << 512


class Server(ForkingMixIn, TCPServer):
    pass


class Handler(BaseRequestHandler):

    def handle(self):
        client = self.request
        client.settimeout(50.0)

        client.sendall("Give me your prime and I will put the flag into it!\n")

        try:
            p = int(self.read_line(client))
        except:
            client.sendall("hacker?\n")
            return

        if not ((1 << 100) < p < (1 << 200)):
            client.sendall("out of bounds\n")
            return

        if not self.check_prime(p):
            client.sendall("not a prime\n")
            return

        client.sendall("Give me your base:\n")

        try:
            g = int(self.read_line(client)) % p
            if g <= 1 or g >= p - 1:
                raise
        except:
            client.sendall("hacker?\n")
            return

        res = pow(g * FLAG, FLAG, p) * FLAG + FLAG
        res %= p

        client.sendall("Whew, here it is: %s\n" % res)
        return

    def check_prime(self, p):
        """Miller-Rabin test"""
        if p & 1 == 0:
            return False

        m = p - 1
        s = 0
        while m & 1 == 0:
            m >>= 1
            s += 1

        for j in range(100):
            a = random.randint(2, p - 2)
            if gcd(a, p) != 1:
                return False

            b = pow(a, m * (1 << s), p)
            if b in (0, 1, p - 1):
                continue

            for i in range(s):
                b = pow(b, 2, p)

                if b == 1:
                    return False

                if b == p - 1:
                    if i < s - 1:
                        break
                    else:
                        return False
            else:
                return False
        return True

    def read_line(self, client):
        line = ""
        while "\n" not in line:
            s = client.recv(1)
            if not s:
                break
            line += s
        return line


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    Server.allow_reuse_address = True
    Server(("0.0.0.0", 3120), Handler).serve_forever()
