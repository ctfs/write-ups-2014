#!/usr/bin/env python

import socket
 
s = socket.socket()
s.connect(("asis-ctf.ir", 12445))
 
print s.recv(2048)
s.send("Paillier\n")
print s.recv(2048)

# get the secret for later use
secret = s.recv(2048)
print secret
secret = secret.split()[3]

# initialize an upperlimit close to the real upperlimit
# note that we are searching n**2. In hindsight it might
# have been easier and faster to search for n (fewer bits)
up = 10**600
limitsearch = True
#look for the limits
while limitsearch:
    print "upperlimit = %s" %up
    s.sendall("D\n")
    s.recv(2048)
    s.sendall("%s\n" %up)
    result = s.recv(2048)
    # printing server output for debugging purposes
    print result
    if "Your original message is" in result:
        print "raise limits"
        lo = up
        up = up*10
    else:
        print "limits found:\n"
        print "upperlimit:%s\n" %up
        limitsearch = False
    s.recv(2048)


print "\n\n\nsearching n**2:\n\n"
nsearch = True
#search n**2 between our limits
while nsearch:
    n2 = (lo + up) // 2
    print "n**2 = %s" %(n2)
    s.sendall("D\n")
    s.recv(2048)
    s.sendall("%s\n" %n2)
    result = s.recv(2048)
    print result
    if "Your original message is" in result:
        print "raise lowerlimit"
        lo = n2
    elif "Your secret is too long" in result:
        print "lower upperlimit"
        up = n2
    else:
        print "found n**2: ", lo+2
        nsearch = False
    if (lo == up) or (lo+1 == up):
        n2 = (lo + up) // 2
        print "found n**2: ", lo+2
        nsearch = False
    s.recv(2048)

#decrypting the secret
m2 = 1
n2 = lo+2
s.sendall("E\n")
print s.recv(2048)
s.sendall("%s\n" %m2)
em2 = s.recv(2048)
print em2
em2 = em2.split()[3]
print s.recv(2048)
s.sendall("D\n")
print s.recv(2048)
todecrypt = int(secret)*int(em2)%n2
s.sendall("%s\n" %todecrypt)
result = s.recv(2048)
print result
result = int(result.split()[4])-1
print hex(result)[2:-1].decode('hex')
