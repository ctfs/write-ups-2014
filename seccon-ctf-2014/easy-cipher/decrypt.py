import sys
import binascii
import string

def loadlist(infile):
	tlist = []
	for line in open(infile,'r'):
		for w in line.split(): tlist.append(w.lower())
	return tlist

# first argument: binary/octal/decimal/hexadecimal input
if len(sys.argv) != 2: sys.exit(2)

words = loadlist(sys.argv[1])
chars = set('abcdef')
msg = ''
for w in words:
	try:
		msg+=binascii.unhexlify('%x' % int(w,2))
	except (ValueError, TypeError) as e:
		if any((c in chars) for c in w):
			msg+=w.decode('hex')
			continue
		if w[0] == '0':
			msg+=chr(string.atoi(w, base=8))
			continue
		msg+=chr(int(w))
print msg
