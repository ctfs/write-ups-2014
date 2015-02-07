# Sharif University Quals CTF 2014: Rolling Hash

**Category:** Cryptography
**Points:** 30
**Solves** 212
**Description:**

>
>```python
>flag="*********"
>def RabinKarpRollingHash( str, a, n ):
>	result = 0
>	l = len(str)
>	for i in range(0, l):
>		result += ord(str[i]) * a ** (l - i - 1) % n
>	print "result = ", result
>
>RabinKarpRollingHash(flag, 256, 10**30)
>```
> output is 
> 1317748575983887541099 
> What is the flag?

## Write-up

The flag variable suggests that the flag is of length 9, the biggest decimal value a single character can have is `127`.
Combining both, we see that `result` can has at maximum `127\*256\*\*8`, which is `2.3427365e+21`. As we see, the modulu by n, a 31 digit number, does not have any effect, so we can leave that part out.

We just have to reverse the encryption process by dividing the given `result` by the relative multiplication of `a`. The rest is used in the further computation of each following letter. See the [decryption and encryption code](code.py).
## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/13/>
