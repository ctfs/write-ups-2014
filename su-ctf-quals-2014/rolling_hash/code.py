def RabinKarpRollingHash( string, a, n ):
	result = 0
	l = len(string)
	for i in range(0, l):
		result += ord(string[i]) * a ** (l - i - 1)
	print "result = ", result

def DeRabinKarpRollingHash( string, cipher , a ):
	result=''
	for i in range(len(string),-1,-1):
		amulaitimes=a**i
		result+=chr(cipher/amulaitimes)
		cipher=cipher%amulaitimes
	print "result = ", result

flag="*********"
flag="Good Luck"
RabinKarpRollingHash(flag, 256, 10**30)
output=1317748575983887541099
DeRabinKarpRollingHash(flag, output, 256)
