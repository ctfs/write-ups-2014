# ASIS Cyber Security Contest Finals 2014: Lottery

**Category:** Web
**Points:** 100
**Description:**

> Go here:
>
> <http://asis-ctf.ir:12437/>

## Write-up

The web site says:

> The 1234567890th visitor, the prize awarded.
> Anyone who has visited our site is the 1234567890th Special prizes are awarded.
> You are the 717 visitor
> Don't hack cookies, we are alive :)

The site sets a cookie named Visitor with the following contents:

```
NzE3Ojc4OGQ5ODY5MDU1MzNhYmEwNTEyNjE0OTdlY2ZmY2Ji
```

This is the base64-encoded version of the string `717:788d986905533aba051261497ecffcbb`, i.e., the visitor count followed by the MD5 hash for that number.

What is the MD5 hash for `1234567890`?

```bash
$ md5 -s '1234567890'
MD5 ("1234567890") = e807f1fcf82d132f9bb018ca6738a19f
```

So, let’s set the cookie value to the base64-encoded version of:

```
1234567890:e807f1fcf82d132f9bb018ca6738a19f
```

…which is:

```bash
$ base64 <<< '1234567890:e807f1fcf82d132f9bb018ca6738a19f'
MTIzNDU2Nzg5MDplODA3ZjFmY2Y4MmQxMzJmOWJiMDE4Y2E2NzM4YTE5Zgo=
```

Refreshing the page now reveals the following message:

> The 1234567890th visitor, the prize awarded.
> Anyone who has visited our site is the 1234567890th Special prizes are awarded.
> the flag is: ASIS_9f1af649f25108144fc38a01f8767c0c

And indeed, `ASIS\_9f1af649f25108144fc38a01f8767c0c` is the flag.

## Other write-ups and resources
* <http://dhanvi1.wordpress.com/2014/10/24/lottery-asis-ctf-2014-web-100-writeup/>
* <http://www.mrt-prodz.com/blog/view/2014/10/asis-ctf-finals-2014---lottery-100pts-writeup>
* <https://hackucf.org/blog/asis-2014-web-100-lottery/>
* <https://beagleharrier.wordpress.com/2014/10/13/asis-ctf-finals-2014lottery-writeup/>
* <http://bruce30262.logdown.com/posts/237386-asis-ctf-finals-2014-how-much-exactly-lottery>
* <http://barrebas.github.io/blog/2014/10/31/asis-ctf-lottery/>
