#!/usr/bin/env python

import sys, socket, struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
print s.recv(1024)

contents = open(sys.argv[3], "rb").read()
s.send(struct.pack("<I", len(contents)) + contents)

print "The challenge server says: ", s.recv(1024)
