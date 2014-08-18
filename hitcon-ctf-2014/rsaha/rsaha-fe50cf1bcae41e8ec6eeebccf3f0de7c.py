#!/usr/bin/env python

import random
import select
import signal
import sympy
import sys


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def random_prime(bits):
    return sympy.nextprime(2 ** bits + random.randint(0, 2 ** bits))


def encrypt(bits, m):
    p = random_prime(bits)
    q = random_prime(bits)
    n = p * q
    assert m < n
    print n
    print m ** 3 % n
    print (m + 1) ** 3 % n


def main():
    signal.alarm(180)
    sys.stdout = Unbuffered(sys.stdout)
    for i in range(1, 10):
        bits = 50 * i
        m = random.randint(0, 4 ** bits)
        encrypt(bits, m)
        rfd, _, _ = select.select([sys.stdin], [], [], 10)
        if rfd:
            try:
                x = int(raw_input())
            except ValueError:
                print "\033[31;1mEnter a number, ok?\033[0m"
                exit()
            if x == m:
                print "\033[32;1mGreat:)\033[0m"
                continue
            else:
                print "\033[31;1mso sad :(\033[0m"
                exit()
        else:
            print "\033[31;1mToo slooooooooooow :(\033[0m"
            exit()

    bits = 512.512
    m = int(open('flag').read().encode('hex'), 16)
    encrypt(bits, m)
    print "\033[32;1mGood Luck!\033[0m"


if __name__ == '__main__':
    main()
