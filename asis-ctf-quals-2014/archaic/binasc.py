#!/usr/bin/python

import sys


fileRes = open("finalres.txt", 'rb')
binenc = fileRes.read().replace(',', '').replace(' ', '')
binenc = binenc[1:]
# decode the binary to ascii
print (hex(int((binenc),2))[2:][:-1]).decode('hex')
