# ASIS Cyber Security Contest Quals 2014: Archaic

**Category:** Crypto
**Points:** 300
**Description:**

> [file](crypto_300_5e5d1adf0bb2ca58131ca28878a4b907)

## Write-up

I started to 'crack' this challenge long after the CTF but luckily for us this challenge is completely offline. You get everything you need from the [given source file](crypto_300_5e5d1adf0bb2ca58131ca28878a4b907).

When you open the source file (and after you unpack it) you'll see that you're given 3 files (I've also included these in the write-up):

* [A python script](archaic.py)

* [A public key](pubKey.txt)

* [An encrypted message](enc.txt)


So let's start by studying the python code. The most important thing here is not the encryption method but rather the method of how the encryption keys are made. 

```python
def makeKey(n):
	privKey = [random.randint(1, 4**n)]
	s = privKey[0]
	for i in range(1, n):
		privKey.append(random.randint(s + 1, 4**(n + i)))
		s += privKey[i]
	q = random.randint(privKey[n-1] + 1, 2*privKey[n-1])
	r = random.randint(1, q)
	while gmpy2.gcd(r, q) != 1:
		r = random.randint(1, q)
	pubKey = [ r*w % q for w in privKey ]
	return privKey, q, r, pubKey
```

If you analyze this you might notice this is a [Merkle-Hellman cryptosystem](http://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem), this is also easy to find by googling a snippet of the code. The Merkle-Hellman cryptosystem is a very old cryptosystem and has already been broken. So all that's left for us to do, is to find the attack method and try that on our encrypted message.

The attack method makes use of some complicated math but I'll try to explain the general idea. If you want to know the details I refer you to the [included paper](Merkle_Hellman_Attacks.pdf) or you can find plenty of other research and papers online.

The basic idea is that you make a large matrix `A` of the following form:

```
| I(nxn)  O(nx1) |
| P(1xn) -C(1x1) |
```

Where `I` represents an Identity matrix, `O` a matrix full of `0`, `P` is your public key and `C` is your encrypted message. The numbers between parentheses are the dimensions of the matrix with `n` representing the length of the public key. If you use the LLL lattice reduction algorithm on this matrix you should get short vectors spanned by this matrix. Among those short vectors is a possible solution to the encryption problem (if you encrypt that solution with the public key you would get the same encrypted message). To find that solution between all those vectors you need to look for a vector which consists of only `1's` and `0's`. Why `1's` and `0's`? Because that's how the encrypted message is created. It takes the binary bits of your text and multiplies them with the public key. This is effectively the same as multiplying a vector of `1's` and `0's` with the public key vector. 

Now we need to create that matrix I proposed and we need to create/use the LLL lattice reduction algorithm. Since the LLL algorithm is complicated and long I tried to find one for python unfortunately my search was unsuccessful. I did however find a program called [sage](http://www.sagemath.org/). This program comes with a lot of mathematical functions including the LLL algorithm. The beautiful part of it is you can import it in python as a library. I opted to use the cloud application of sage but normally the code should be the same.

[The code I used in sage](sage.py) looks like:

```python
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
```

Then you need to search the correct vector in the created text file. It is important to note that the last number (`0` or `1`) is not part of the message and should be dropped. [Encode the binary to ascii and you get the flag](binasc.py).

The flag is `ASIS_9bd3d5fd2422682c19568806a07061ce`.

## Other write-ups and resources

* none yet
