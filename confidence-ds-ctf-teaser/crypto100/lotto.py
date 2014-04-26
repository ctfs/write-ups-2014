from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime
import random
import os
import time
import sys

flag = open('flag.txt').read()

# config
start_money = 100
cost = 5     # coupon price
reward = 100 # reward for winning
maxNumber = 1000 # we're drawing from 1 to maxNumber
screenWidth = 79

intro = [
	'',
	'Welcome to our Lotto!',
	'Bid for $%d, win $%d!' % (cost, reward),
	'Our system is provably fair:',
	'   Before each bid you\'ll receive encrypted result',
	'   After the whole game we will reveal the key to you',
	'   Then, you can decrypt results and verify that we haven\'t cheated on you!',
	'    (e.g. by drawing based on your input)',
	''
	]

# expand to AES block with random numeric salt
def randomExtend(block):
	limit = 10**(16-len(block))
	# salt
	rnd = random.randrange(0, limit)
	# mix it even more
	rnd = (rnd ** random.randrange(10, 100)) % limit
	# append it to the block
	return block + ('%0'+str(16-len(block))+'x')%rnd

def play():
	# print intro
	print '#' * screenWidth
	for line in intro:
		print  ('# %-' + str(screenWidth-4) + 's #') % line
	print '#' * screenWidth
	print ''

	# prepare everything
	money = start_money

	key = Random.new().read(16) # slow, but secure
	aes = AES.new(key, AES.MODE_ECB)

	# main loop
	quit = False
	while money > 0:
		luckyNumber = random.randrange(maxNumber + 1) # fast random should be enough
		salted = str(luckyNumber) + '#'
		salted = randomExtend(salted)

		print 'Your money: $%d' % money
		print 'Round verification: %s' % aes.encrypt(salted).encode('hex')
		print ''
		print 'Your choice:'
		print '\t1. Buy a coupon for $%d' % cost
		print '\t2. Withdraw your money'
		print '\t3. Quit'

		# read user input
		while True:
			input = raw_input().strip()
			if input == '1':
				# play!
				money -= cost
				sys.stdout.write('Your guess (0-%d): ' % maxNumber)
				guess = int(raw_input().strip())
				if guess == luckyNumber:
					print 'You won $%d!' % reward
					money += reward
				else:
					print 'You lost!'
				break
			elif input == '2':
				# withdraw
				if money > 1337:
					print 'You won! Here\'s your reward:', flag
				else:
					print 'You cannot withdraw your money until you get $1337!'
				break
			elif input == '3':
				quit = True
				break
			else:
				print 'Unknown command!'

		print 'The lucky number was: %d' % luckyNumber
		if quit:
			break
		print '[enter] to continue...'
		raw_input()

	print 'Verification key:', key.encode('hex')
	if money <= 0:
		print 'You\'ve lost all your money! get out!'

if __name__ == '__main__':
	play()
