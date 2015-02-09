#!/usr/bin/env python
# coding=utf-8
import sys

def reverse(led):
	if len(led) != 8:
		return None
	orig = [None, None, None, None, None, None, None, None]
	led[0] = int(not(int(led[0])))
	led[1] = int(not(int(led[1])))
	led[2] = int(not(int(led[2])))
	led[3] = int(not(int(led[3])))
	led[4] = int(not(int(led[4])))
	led[5] = int(not(int(led[5])))
	led[6] = int(not(int(led[6])))
	led[7] = int(not(int(led[7])))
	# 3 = !led3
	orig[2] = int(not(led[2]))
	# 2 = !led2
	orig[1] = int(not(led[1]))
	# 4 = 2 ^ led7
	orig[3] = orig[1] ^ led[6]
	# 7 = 2 ^ led5
	orig[6] = orig[1] ^ led[4]
	# 5 = (2^3) ^ led8
	orig[4] = orig[1] ^ orig[2] ^ led[7]
	# 6 = (2^4) ^ led6
	orig[5] = orig[1] ^ orig[3] ^ led[5]
	# led4 = (3^2)^(6^8) > (6^8) = (3^2)^led4 > 8 = ((3^2)^led4)^6
	orig[7] = orig[2] ^ orig[1] ^ led[3] ^ orig[5]
	# 1 = led1 ^ (6^8)
	orig[0] = led[0] ^ orig[5] ^ orig[7]

	orig[0] = str(int(not(orig[0])))
	orig[1] = str(int(not(orig[1])))
	orig[2] = str(orig[2])
	orig[3] = str(orig[3])
	orig[4] = str(int(not(orig[4])))
	orig[5] = str(orig[5])
	orig[6] = str(int(not(orig[6])))
	orig[7] = str(orig[7])
	return orig

finalhex = ''
cipher = 'BQDykmgZ0I6SaQnq4o/iEONudetXdPJdpl1UVSlU69oZOtvqnHfinOpcEfIjXy9okkVpsuw2kpKS=='.decode('base64')
f = open('base64.bin', 'wb')
f.write(cipher)
f.close()
f = open('base64.bin', 'rb')
try:
	byte = f.read(1).encode('hex')
	while byte != '':
		binarybyte = format(int(byte, 16), '#010b')[2:]
		decryptedbyte = reverse(list(binarybyte)[::-1])
		decryptedbyte = ''.join(decryptedbyte)[::-1]
		finalhex = finalhex + str(hex(int(decryptedbyte,2))[2:].zfill(2))
		byte = f.read(1).encode('hex')
finally:
	f.close()

print finalhex
f = open('decrypted.bin', 'wb')
f.write(finalhex.decode('hex'))
f.close()
