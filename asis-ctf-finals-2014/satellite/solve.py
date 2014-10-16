#!/usr/bin/env python
# coding=utf-8

import re
from pwn import * # https://github.com/Gallopsled/pwntools
import pycosat

s = remote('asis-ctf.ir', 12435)
s.recvline()
s.recvline()
s.recvline()
s.sendline('Sattelite')
numVars = 5
while True:
	eq = s.recvline().replace('(', '').replace(')', '').replace('x', '').replace('¬', '-')
	print eq
	eqs = eq.split('∧')
	forPicosat = []
	for curEq in eqs:
		tmp = re.findall('-?\d+', curEq)
		tmp = map(int, tmp)
		forPicosat.append(tmp)

	solution = ''
	for x in pycosat.solve(forPicosat):
		if x < 0:
			solution += '0'
		else:
			solution += '1'

	solution = solution.ljust(numVars, '0')
	numVars += 1

	s.sendline(solution)
	print s.recvline()
