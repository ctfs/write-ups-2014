import sys
if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " <inputfile>"
	sys.exit(1)
fi=open(sys.argv[1], 'r')
N=int(fi.read())
fi.close()
H=hex(N)[2:][:-1]
fo=open('out.hex', 'wb')
fo.write(''.join([chr(int(H[i:i+2],16)) for i in range(0, len(H), 2)]))
fo.close()
