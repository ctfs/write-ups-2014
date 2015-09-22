# ASIS Cyber Security Contest Finals 2014: Ultra Secure

**Category:** Crypto
**Points:** 400
**Description:**

> Connect there:
>
> ```bash
> nc asis-ctf.ir 12445
> ```

## Write-up

First let's connect to the service and see what we need to do

```bash
$ nc asis-ctf.ir 12445

    Here we use a well-known cryptosystem, which introduced in late 90s as a part of PhD Thesis. This cryptosystem is a probabilistic asymmetric algorithm, so computer nerds are familiar with the basics. The power of this cryptosystem is based on the fact that no efficient general method for computing discrete logarithms on conventional computers is known. In real world it could be used in a situation where there is a need for anonymity and a mechanism to validate, like election.
What's the name of this cryptosystem?
```

If you google some of key features of this cryptosystem we quickly come to the conclusion that this is a [Paillier cryptosystem](http://en.wikipedia.org/wiki/Paillier_cryptosystem). Answering Paillier gives us new information.

```bash
$ nc asis-ctf.ir 12445

...

What's the name of this cryptosystem?
Paillier
The secret is: 45710623737087701711820134797542238364727935815041561117965550719730211404995880962189849763186419941404256428269541230638298594081804054803929405338706331501510355769791788035782101048794197150178174026969607210826909631760346060869225182396182048777369368142016863385200586265163953840808342248328628488558966204179925698305553258440383522033840372138701862745580428470631799476191017336213672662419943702985732053645939959855799510630518494500337262650866518227631714070805564029135334485129969768206948775297659476280347999959347004640627153560223776086816027050734375066512946795924861244218488564290260122095
Tell us your choise:
------------------------
[E]ncrypt: [D]ecrypt:
```

It seems like we can encrypt and decrypt messages and we can but there are some limitations: 
*   We can only encrypt/decrypt integers
*   We can't decrypt the secret (duh it's likely the flag)
*   We can't decrypt/encrypt really large numbers. 

An interesting feature of the Paillier system is the [Homomorphic properties](http://en.wikipedia.org/wiki/Paillier_cryptosystem#Homomorphic_properties). This identity is really usefull:

```
D(E(m_1, r_1)*E(m_2, r_2) % n**2) = m_1 + m_2 % n
```

This means we can know `D(secret) + m_2` by decrypting the encrypted version of `m_2` multiplied with `secret`. But since we can't decrypt large numbers (and `secret*E(m_2)` will be very large) we will need to find `n**2` so the program can decrypt it. To do that we will have to find the highest decryptable number since the number higher than that one will be `n**2`. Note you can also search for the highest encryptable number and this will result in `n`. I used a [script](getflag.py) to search for `n**2`. The way we searched for `n**2` is seperated in steps. First we search for the size of `n**2`

```python
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
```

After we've found the size we can use a [binary search algorithm](http://en.wikipedia.org/wiki/Binary_search_algorithm) to efficiently find our n, below is the python snippet

```python
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
        print "found n**2: ", n2+2
        nsearch = False
    if (lo == up) or (lo+1 == up):
        print "found n**2: ", n2+2
        nsearch = False
    s.recv(2048)
```

The script gives us the following `n**2`

```
312297583190587351458137431380785408561144079636591681208619346428876861270850912733847184254477966663881634771561389507014978092603348639752023175244091649730048589982867752333512863931604180416460758858834247438893704154885898939981322625658760458931477676038950504043387828218684225085126061041045616606366038003171348569328265909629270290356532433942132981636025919553658034062710641354232206614287339987328297437585450601990328499529000849761619575357764721850032262663234053608997621038879298169658587018163190471754083729630359432041430309138927003684672819536681979821421566465558117262044624406325139876689
```

All thats left to do is encrypt a simple number like `1` multiply the secret thats given at the start with this encrypted `1` take modulo `n**2`  of the calculated number and give the result back for decryption. That decrypted message is your flag + `1`. You'll be left over with an integer so translate the integer to hex and decode the hex to ascii for your flag. 

```python
m2 = 1
n2 = n2+2
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

```

The flag is `ASIS_85c9febd4c15950ab1f19a6bd7a94f85`.

## Other write-ups and resources

* <http://tasteless.eu/2014/10/asis-ctf-finals-2014-ultra-secure-crypto-400/>
* <http://bt3gl.github.io/on-paillier-binary-search-and-the-asis-ctf-2014.html>
* <http://blog.dragonsector.pl/2014/10/asis-ctf-finals-2014-ultra-secure.html>
* [Exploit written in Python](http://pastebin.com/LsMRp71Y)
* <https://beagleharrier.wordpress.com/2014/10/15/asis-ctf-finals-2014ultra-secure-writeup/>
