# HITCON CTF 2014: rsaha

**Category:** Crypto
**Points:** 200
**Description:**

> Can you break RSA?
> [https://dl.dropbox.com/s/xqkoamfvas1rdb7/rsaha-fe50cf1bcae41e8ec6eeebccf3f0de7c.py](rsaha-fe50cf1bcae41e8ec6eeebccf3f0de7c.py)
> [http://ctf.tw/rsaha-fe50cf1bcae41e8ec6eeebccf3f0de7c.py](rsaha-fe50cf1bcae41e8ec6eeebccf3f0de7c.py)
>
> ```bash
> $ nc 54.64.40.172 5454
> ```

## Write-up

By studying the given code we learn that we have to give the program the correct number and after 10 times it will give us the flag. The most impportant part is the following:

```
def encrypt(bits, m):
    p = random_prime(bits)
    q = random_prime(bits)
    n = p * q
    assert m < n
    print n
    print m ** 3 % n
    print (m + 1) ** 3 % n
```

The programs gives us `n`, `m**3 %n` and `(m+1)**3 %n` and asks us `m` in return. After some research on rsa encryption we notice we can break this encryption because we are given two encrypted message. We know those message are related to each other and encrypted using the same key. This is also known as a [Franklin-Reiter Related Message Attack](http://en.wikipedia.org/wiki/Coppersmith%27s_Attack). This lead us to the next formula:

```
((m + 1)**3 +  2*m**3 - 1)/((m + 1)**3 - m**3 + 2) = m mod n
``` 

After a while I figured out we can use the extended euclidean algorithm to calculate m from this formula. Here is a piece of the python code I wrote:

```
# return a triple (g, x, y), such that ax + by = g = gcd(a, b).
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

.
.
.

m_n1 = m_31 + 2*m_3 - 1
m_n2 = m_31 - m_3 + 2
f = m_n1%n
g = m_n2%n
sol1 = egcd(f,n)
sol2 = egcd((1-n*sol1[2])*g/f,n)
m = sol2[1]
m2 = -m
if m < 0:
	m += n
#if it's not really m its the mod inv of m
if (m ** 3 % n) != m_3:
	m = m2
if m < 0:
    m += n

```

This decrypts our given strings into the message we need to return. Finally the program gave us a final message holding the key. Of course we had to decrypt that one too.

The flag is `HITCON{RSA is a really secure algorithm, right?}`.




## Other write-ups

* none yet
