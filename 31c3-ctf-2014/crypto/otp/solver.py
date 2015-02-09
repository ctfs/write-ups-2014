#!/usr/bin/env python2
from hashlib import sha256
import itertools
import struct
import time
import sys

given_user = "admin"
given_otp  = "9ae684ca583214d33905000000000000fd635dded0bbb40e162da79fba55ae32"

given_otp = given_otp.decode("hex")
given_keyid = given_otp[:8]
given_keyid, given_sequence, _, _ = struct.unpack("QQQQ", given_otp)
print "sequence: %d" % given_sequence
print "keyid:    0x%016x" % given_keyid

print "building lookups..."
hash_base = given_user + "\x00"
hash_len = len(given_user) + 8

#xor = lambda a,b: "".join(chr(ord(i) ^ ord(j)) for i,j in zip(a,b))
def hash_byte(b, pos, length):
	s = ("\x00" * pos) + chr(b) + ("\x00" * (length - pos - 1))
	return struct.unpack("Q", sha256(s).digest()[:8])[0]

lala = given_keyid
lala ^= hash_byte(0, 0, hash_len)
for p, c in enumerate(hash_base):
	lala ^= hash_byte(ord(c), p, hash_len)
#lala is now the value we are searching when producing the bytewise sha256 for the remaining 7 positions
possible_hash_products = {}
for p in xrange(len(hash_base), hash_len):
	possible_hash_products[p] = tuple(hash_byte(c, p, hash_len) for c in xrange(256))

#we now create 2 lists with the products from position [-3:-1] and [-6:-4]
products = []
for prod in xrange(2):
	product = []
	for a,b,c in itertools.product(possible_hash_products[hash_len - 3 - (3 * prod)], possible_hash_products[hash_len - 2 - (3 * prod)], possible_hash_products[hash_len - 1 - (3 * prod)]):
		product.append(a^b^c)
	products.append(product)

#we now calculate the product of lala together with the first unknown position
product = []
for prod in possible_hash_products[len(hash_base)]:
	product.append(prod ^ lala)
products.append(product)

products0set = set(products[0])
#we now have to work with the 3 products and find a combination being 0

print "combining..."
t = time.time()
try:
	for a_pos, a in enumerate(products[2]):
		#this is a speedup for me, normally requires ~4.5s * 193 = ~15min on my machine
		#if a_pos < 0xbe:
		#	continue
		t2 = time.time()
		print "\r%d/255 (%f)" % (a_pos, t2 - t),
		sys.stdout.flush()
		t = t2
		for b_pos, b in enumerate(products[1]):
			if a^b in products0set:
				c_pos = products[0].index(a^b)
				secret = chr(a_pos) + chr((b_pos >> 16) & 255) + chr((b_pos >> 8) & 255) + chr(b_pos & 255) + chr((c_pos >> 16) & 255) + chr((c_pos >> 8) & 255) + chr(c_pos & 255)
				1/0
except ZeroDivisionError:
	pass
print
print "secret: ??%s" % secret.encode("hex")

for first in xrange(256):
	tmp = chr(first) + secret
	if sha256(struct.pack("Q", given_sequence) + tmp).digest()[:16] == given_otp[-16:]:
		secret = tmp
		break
print "secret: %s" % secret.encode("hex")
produced_otp = struct.pack("QQ", given_keyid, given_sequence + 1) + sha256(struct.pack("Q", given_sequence + 1) + secret).digest()[:16]
print "next otp: %s" % produced_otp.encode("hex")

