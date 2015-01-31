#!/usr/bin/python
from math import sin
from urlparse import parse_qs
from base64 import b64encode
from base64 import b64decode
from re import match

SALT = ''
USERS = set()
KEY = ''.decode('hex')

def xor(a, b):
	return ''.join(map(lambda x : chr(ord(x[0]) ^ ord(x[1])), zip(a, b * 100)))

def hashme(s):
	#my secure hash function
	def F(X,Y,Z):
		return ((~X & Z) | (~X & Z)) & 0xFFFFFFFF
	def G(X,Y,Z):
		return ((X & Z) | (~Z & Y)) & 0xFFFFFFFF
	def H(X,Y,Z):
		return (X ^ Y ^ Y) & 0xFFFFFFFF
	def I(X,Y,Z):
		return (Y ^ (~Z | X)) & 0xFFFFFFFF
	def ROL(X,Y):
		return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

	A = 0x67452301
	B = 0xEFCDAB89
	C = 0x98BADCFE
	D = 0x10325476
	X = [int(0xFFFFFFFF * sin(i)) & 0xFFFFFFFF for i in xrange(256)]

	for i,ch in enumerate(s):
		k, l = ord(ch), i & 0x1f
		A = (B + ROL(A + F(B,C,D) + X[k], l)) & 0xFFFFFFFF
		B = (C + ROL(B + G(C,D,A) + X[k], l)) & 0xFFFFFFFF
		C = (D + ROL(C + H(D,A,B) + X[k], l)) & 0xFFFFFFFF
		D = (A + ROL(D + I(A,B,C) + X[k], l)) & 0xFFFFFFFF

	return ''.join(map(lambda x : hex(x)[2:].strip('L').rjust(8, '0'), [B, A, D, C]))

def gen_cert(login):
	global SALT, KEY
	s = 'login=%s&role=anonymous' % login
	s += hashme(SALT + s)
	s = b64encode(xor(s, KEY))
	return s

def register():
	global USERS
	login = raw_input('Your login: ').strip()
	if not match('^[\w]+$', login):
		print '[-] Wrong login'
		return
	if login in USERS:
		print '[-] Username already exists'
	else:
		USERS.add(login)
		print '[+] OK\nYour auth certificate:\n%s' % gen_cert(login)

def auth():
	global SALT, KEY
	cert = raw_input('Provide your certificate:\n').strip()
	try:
		cert = xor(b64decode(cert), KEY)
		auth_str, hashsum = cert[0:-32], cert[-32:]
		if hashme(SALT + auth_str) == hashsum:
			data = parse_qs(auth_str, strict_parsing = True)
			print '[+] Welcome, %s!' % data['login'][0]
			if 'administrator' in data['role']:
				flag = open('flag.txt').readline()
				print flag
		else:
			print '[-] Auth failed'
	except:
		print '[-] Error'


def start():
	while True:
		print '======================'
		print '[0] Register'
		print '[1] Login'
		print '======================'
		num = raw_input().strip()
		if num == '0':
			register()
		elif num == '1':
			auth()

start()
