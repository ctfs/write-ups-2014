# open the public key and strip the spaces so we have a decent array
fileKey = open("pubKey.txt", 'rb')
pubKey = fileKey.read().replace(' ', '').replace('L','').split(',')
nbit = len(pubKey)
# open the encoded message
fileEnc = open("enc.txt", 'rb')
encoded = fileEnc.read().replace('L','')
print "start"
# create a large matrix of 0's (dimensions are public key length +1)
A = Matrix(ZZ,nbit+1,nbit+1)
# fill in the identity matrix
for i in xrange(nbit):
    A[i,i] = 1
# replace the bottom row with your public key
for i in xrange(nbit):
    A[i,nbit] = pubKey[i]
# last element is the encoded message
A[nbit,nbit] = -int(encoded)

res = A.LLL()
resfil = open("res.txt", 'wb')
resfil.write(res.str())

# print solution
M = res.row(295).list()
print M
