#!/usr/bin/env python
# coding=utf-8

from pwn import * # https://github.com/Gallopsled/pwntools

r = remote('number.quals.seccon.jp', 31337)

while True:
	numbers = r.recvline()
	print numbers
	if 'Congrat' in numbers:
		print r.recvall()
		break
	numbers = numbers.split(',')
	numbers = map(int, numbers)
	x = r.recvuntil('number?')
	print x
	if 'maximum' in x:
		answer = max(numbers)
	elif 'minimum' in x:
		answer = min(numbers)
	else:
		print 'else'
		print r.recvline()

	answer = str(answer)
	print '>>> %s' % answer
	r.sendline(answer)
