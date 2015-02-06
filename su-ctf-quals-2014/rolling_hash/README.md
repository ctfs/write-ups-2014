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

(TODO)

## Other write-ups and resources

* none yet
