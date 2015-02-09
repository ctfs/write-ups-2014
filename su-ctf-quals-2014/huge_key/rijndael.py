import sys
import base64
from Crypto.Cipher import AES

# ./arg0 ciphertxt.bin
if len(sys.argv) != 2: sys.exit(2)

fbytes = open(sys.argv[1],"r").read()
# len(iv) = 16
iv=fbytes[:16]
fbytes=fbytes[16:]

key=''
AES.key_size=16 # as seen in the original php file

for i in range(0,256):
	for j in range(0,256):
		key = ('{:02x}'.format(i) + '{:02x}'.format(j) + str('0'*28)).decode('hex')
		#sys.stdout.write(key) # debug output, you can also parse it to detect the flag
		c=AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
		msg = c.decrypt(fbytes)
		if 'flag' in msg: print msg
