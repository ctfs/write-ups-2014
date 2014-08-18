#!/usr/bin/env python

import random
import select
import signal
import sympy
import sys
import math
import socket

# return a triple (g, x, y), such that ax + by = g = gcd(a, b).
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


HOST, PORT = '54.64.40.172', 5454
# SOCK_STREAM == a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setblocking(0)  # optional non-blocking
sock.connect((HOST, PORT))
count = 1
counter = 0
flag = 0
while True:
    receive = sock.recvfrom(1024)
    print receive[0].split('\n')
    if count == 1:
            n = int(receive[0].split('\n')[0+counter])
            print "n: %s" % n
            count = 2
    if counter == 0:
        receive = sock.recvfrom(1024)
        print receive[0].split('\n')
    if count == 2:
            m_3 = int(receive[0].split('\n')[1+counter])
            print "m3: %s" % m_3
            m_31 = int(receive[0].split('\n')[2+counter])
            print "m3+1: %s" % m_31
            count = 3
    if count == 3:
        m_n1 = m_31 + 2*m_3 - 1
        m_n2 = m_31 - m_3 + 2
        f = m_n1%n
        g = m_n2%n
        sol1 = egcd(f,n)
        sol2 = egcd((1-n*sol1[2])*g/f,n)
        m = sol2[1]
        m2 = -m
        if m < 0:
            m += n
        #if it's not really m its the mod inv of m
        if (m ** 3 % n) != m_3:
            m = m2
            if m < 0:
                m += n
        print "m: %s" %m
        sock.send(str(m) + '\n')
        count = 1
        counter = 1
        print sock.recvfrom(1024)
        print "new: "
