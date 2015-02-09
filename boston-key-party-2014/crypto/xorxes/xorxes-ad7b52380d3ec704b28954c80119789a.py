# -*- coding: utf-8 -*-
import hashlib, struct, sys

def RROT(b, n, wsize):
	# eq to >>>, borrowed from bonsaiviking
    return ((b << (wsize-n)) & (2**wsize-1)) | (b >> n)

def SHA224(m):
	sha224 = hashlib.sha224() 
	sha224.update(m)
	return int(sha224.hexdigest(), 16)

def compress(m, c):
	assert len(m) == 1

	# calc sha224 on m
	x = SHA224(m)

	# rotate c by 28 bits xor with x
	return x ^ RROT(c, 56, 224)

# Xorxes Hash uses message blocks of 8-bits, with a 224-bit chaining variable.
#
#   (m_0)       (m_1)         ... (m_n)  = input message blocks
#     |           |                 |
#   SHA224      SHA224        ... SHA224    
#     |           |                 |
#  V-(+)-[>>>56]-(+)-[>>>56]- ... --+--- = chaining variable 
#
#  chaining variable + (message length mod 24) = hash output
#
def xorxes_hash(m):
	IV = ord('M') ^ ord('i') ^ ord('t') ^ ord('h') ^ ord('r') ^ ord('a')

	c = IV
	for mb in m:
		c = compress(mb, c)
	out = c + ( len(m) % 24 )
	return hex(out)[2:-1]

if  __name__ =='__main__':
	if not len(sys.argv) == 2:
		print "python xorxes.py [message]"
	else:
		print xorxes_hash(sys.argv[1])