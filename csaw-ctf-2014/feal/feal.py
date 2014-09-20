import os
import array
import binascii
import SocketServer
import base64 as b64
from hashlib import sha1
DEBUG= False
def rot3(x):
    return ((x<<3)|(x>>5))&0xff


def gBox(a,b,mode):
    return rot3((a+b+mode)%256)
def fBox(plain):
    t0 = (plain[2] ^ plain[3])
    y1 = gBox(plain[0] ^ plain[1], t0, 1)
    y0 = gBox(plain[0], y1, 0)
    y2 = gBox(t0, y1, 0)
    y3 = gBox(plain[3], y2, 1)

    return [y3, y2, y1, y0]

def encrypt(plain,subkeys):
    pleft = plain[0:4]
    pright = plain[4:]
    def list_xor(l1,l2):
        return map(lambda x: x[0]^x[1], zip(l1,l2))
    left = list_xor(pleft, subkeys[4])
    right = list_xor(pright, subkeys[5])

    R2L = list_xor(left, right)
    R2R = list_xor(left, fBox(list_xor(R2L, subkeys[0])))

    R3L = R2R;
    R3R = list_xor(R2L, fBox(list_xor(R2R, subkeys[1])))

    R4L = R3R;
    R4R = list_xor(R3L, fBox(list_xor(R3R, subkeys[2])))

    cipherLeft = list_xor(R4L, fBox(list_xor(R4R, subkeys[3])))
    cipherRight = list_xor(cipherLeft, R4R)
    if DEBUG:
        print "PL",pleft
        print "PR",pright
        print "L", left
        print "R", right
        print "R2R",R2R
        print "R2L",R2L
        print "R3R",R3R
        print "R3L",R3L
        print "R4R",R4R
        print "R4L",R4L
        print "CL",cipherLeft
        print "CR",cipherRight
    return cipherLeft+cipherRight

def decrypt(plain,subkeys):
    cipherLeft = plain[0:4]
    cipherRight = plain[4:]

    def list_xor(l1,l2):
        return map(lambda x: x[0]^x[1], zip(l1,l2))
    R4R = list_xor(cipherLeft,cipherRight)
    R4L = list_xor(cipherLeft, fBox(list_xor(R4R, subkeys[3])))


    R3R = R4L
    R3L = list_xor(R4R , fBox(list_xor(R3R, subkeys[2])))

    R2R = R3L
    R2L = list_xor(R3R, fBox(list_xor(R2R, subkeys[1])))

    left = list_xor(R2R, fBox(list_xor(R2L, subkeys[0])))
    right = list_xor(left, R2L)

    pleft = list_xor(left, subkeys[4])
    pright = list_xor(right, subkeys[5])
    if DEBUG:
        print "PL",pleft
        print "PR",pright
        print "L", left
        print "R", right
        print "R2R",R2R
        print "R2L",R2L
        print "R3R",R3R
        print "R3L",R3L
        print "R4R",R4R
        print "R4L",R4L
        print "CL",cipherLeft
        print "CR",cipherRight
    return pleft+pright
def genKeys():
    subkeys=[]
    for x in xrange(6):
        subkeys.append(array.array("B",os.urandom(4)))
    return subkeys
def genNull():
    subkeys=[]
    for x in xrange(6):
        subkeys.append([0]*8)
    return subkeys


class HandleCheckin(SocketServer.BaseRequestHandler):
    def handle(self):
        req = self.request
        proof = b64.b64encode(os.urandom(12))
        req.sendall("You must first solve a puzzle, a sha1 sum ending in 16 bit's set to 1, it must be of length %s bytes, starting with %s\n" % (len(proof)+5, proof))
        test = req.recv(21)
        ha = sha1()
        ha.update(test)
        if (test[0:16] != proof or ord(ha.digest()[-1]) != 0xff
                or ord(ha.digest()[-2]) != 0xff):
            req.sendall("NOPE")
            req.close()
            return

        req.sendall("Welcome to feal 4.3\n")
        key=genKeys()
        kp1 = array.array("B",self.keyPart1)
        kp2 = array.array("B",self.keyPart2)
        kp1="".join(map(chr,encrypt(kp1,key)))
        kp2="".join(map(chr,encrypt(kp2,key)))
        req.sendall("Please decrypt: "+binascii.hexlify(kp1)+binascii.hexlify(kp2)+"\n")
        for x in xrange(2048):
            toEnc=req.recv(8)
            if len(toEnc)!=8:
                req.sendall("Goodbye")
                req.close()
                return
            toEnc=array.array("B",toEnc)
            toSend=binascii.hexlify("".join(map(chr,encrypt(toEnc,key))))
            req.sendall(toSend+"\n")
class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "", int(8888)
    server = ThreadedServer((HOST, PORT), HandleCheckin)
    server.allow_reuse_address = True
    server.serve_forever()