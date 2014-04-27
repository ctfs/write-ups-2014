#!/usr/bin/env python
# coding=utf-8

import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('23.253.207.179', 10001))

known_hashes = {}
count = 0
while True:
	count += 1
	data = s.recv(1024)
	match = re.search('([0-9a-f]{32})', data)
	round_verification_hash = match.group(1)
	match = re.search('Your money: \$(\d+)\s', data)
	money = int(match.group(1))
	print 'Round #%d | Money: $%d | Round verification: %s' % (
		count, money, round_verification_hash
	)
	if money > 1337:
		# Choose “Withdraw your money”, which is now possible. The program will
		# show us the flag before quitting.
		s.send('2\n')
		print s.recv(1024)
		break
	elif round_verification_hash in known_hashes:
		# We’ve seen this hash before, and know which lucky number it maps to.
		s.send('1\n')
		s.recv(1024)
		s.send(known_hashes[round_verification_hash] + '\n')
		print s.recv(1024)
		s.send('\n')
	else:
		# Choose “Withdraw your money”. This fails because we don’t have $1337
		# yet, but it will show us the lucky number which the round verification
		# hash mapped to. Next time we get this hash, we’ll know which number to
		# bet on!
		s.send('2\n')
		data = s.recv(1024)
		match = re.search('The lucky number was: (\d+)\s', data)
		number = match.group(1)
		print 'Lucky number: %s' % number
		known_hashes[round_verification_hash] = number
		s.send('\n')
