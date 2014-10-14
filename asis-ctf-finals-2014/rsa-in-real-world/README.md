# ASIS Cyber Security Contest Finals 2014: RSA in real world!

**Category:** Crypto, Recon
**Points:** 250
**Description:**

> Download [file](rsa_20bdc0fc3b3b06f7a5f920abb4dddfca) and capture the flags!!!

## Write-up

Write-up by [HacknamStyle](http://hacknamstyle.net). Let’s see what [the provided file](rsa_20bdc0fc3b3b06f7a5f920abb4dddfca) could be:

```bash
$ file rsa_20bdc0fc3b3b06f7a5f920abb4dddfca
rsa_20bdc0fc3b3b06f7a5f920abb4dddfca: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < rsa_20bdc0fc3b3b06f7a5f920abb4dddfca > rsa`
* `unxz < rsa_20bdc0fc3b3b06f7a5f920abb4dddfca > rsa`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x rsa_20bdc0fc3b3b06f7a5f920abb4dddfca
```

Let’s find out what the extracted file is:

```bash
$ file rsa
rsa: gzip compressed data, from Unix, last modified: Sun Oct 12 12:02:01 2014
```

The rabbit hole goes deeper…

```bash
$ gunzip < rsa > rsa-unzipped

$ file rsa-unzipped
rsa-unzipped: POSIX tar archive

$ tar vxf rsa-unzipped
x RSA/
x RSA/flag.enc
x RSA/pubkey.pem
```

We have a public key `pubkey.pem` and an encrypted file `flag.enc`. How to obtain the private key to decrypt the flag?

## Factoring the Public Key

Let's use `openssl` to see the public key we are dealing with.

```bash
$ openssl rsa -in pubkey.pem -pubin -text -modulus
Public-Key: (1024 bit)
Modulus:
    00:80:00:00:00:20:00:00:00:00:00:00:00:00:00:
    00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:
    00:00:00:00:00:00:00:00:00:00:00:08:00:00:00:
    02:00:08:00:00:00:02:00:00:00:00:00:00:08:00:
    00:00:00:01:0c:80:00:00:15:e0:00:00:00:00:00:
    00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:
    00:00:00:00:00:00:00:00:00:80:00:00:00:00:0b:
    d0:00:00:00:00:0b:50:00:00:00:00:00:00:00:00:
    00:05:78:00:00:00:00:7b:bb
Exponent: 65537 (0x10001)
Modulus=8000000020000000000000000000000000000000000000000000000000000000000000000000000008000000020008000000020000000000000800000000010C80000015E0000000000000000000000000000000000000000000000000000000000080000000000BD0000000000B500000000000000000000578000000007BBB
```

That modulus contains a lot of zeros. Interestingly, last year there was a [similar RSA challenge in ASIS CTF](http://security.cs.pub.ro/hexcellents/wiki/writeups/asis_rsang). In that challenge they used the bit patterns to guess how the modulus was generated, and relied on that formula to efficiently factorize the modulus. Let's convert the modulus to binary and try to spot all the patterns:

```bash
$ python -c 'print bin(0x8000000020000000000000000000000000000000000000000000000000000000000000000000000008000000020008000000020000000000000800000000010C80000015E0000000000000000000000000000000000000000000000000000000000080000000000BD0000000000B500000000000000000000578000000007BBB)'
0b10000000000000000000000000000000001000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000100000000000000000000000000000000010000000000000100000000000000000000
0000000000000100000000000000000000000000000000000000000000000000000100000000000
0000000000000000000000000000000100001100100000000000000000000000000101011110000
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000001000
0000000000000000000000000000000000000000101111010000000000000000000000000000000
0000000001011010100000000000000000000000000000000000000000000000000000000000000
000000000000000000010101111000000000000000000000000000000000000111101110111011
```

We can spot 14 "chunks" of `1`'s and `0`'s separated by many zeros. These form interesting patterns:

1. `10101111` occurs twice
2. `10110101` occurs _almost_ twice. The second occurrence would be `10111101` but it has an additional `1` in the middle.
3. `111101110111011` is equal to `bin(0b10101111 * 0b10110101)`. This already hints that the formula is of the form `(... + A) * (... + B)` where `A` is `0b10110101`, and `B` is `0b10101111`. After all, the polynomial expansion would end in `(... + A * B)`, and we indeed see this product at the end of the modulus.
4. Interestingly, the chunk `1000011001` is equal to `bin(0b10101111 + 0b10110101 * 0b10)`. This hints that both `A` and `B` where multiplied by an almost equal power of two, and then added (causing the overlap). Potential overlaps also explain the additional `1` in the second occurence of `10110101` (see point 2).

Taking all this together, we have a formula of the form `(... + A) * (... + B)` where `A` is `0b10110101`, and `B` is `0b10101111`. In the polynomial expansion there are two "overlaps" between terms (see point 2 and 4 form the pattern list above). Since there are 14 visible chunks, and two overlaps, we can deduce that the polynomial expansion has 16 terms. Additionally we know that both `A` and `B` each occur three terms in the polynomial expansion (e.g. for `10101111` these are the two occurrences of itself, and in the overlap mentioned in point 4). So finally we get that the modulus was generated by the following formula:

```python
A = 0b10110101
B = 0b10101111
(2**a + 2**b + 2**c + A) * (2**d + 2**e + 2**f + B)
```

Let `a` and `d` be the smallest exponents in each term, and `c` and `d` the second smallest exponent in each term. Once we have this formula, determining the exponents can be done as follows:

1. The first occurrence of `B` in the modulus is caused by `B * 2**51`, so we have `a = 51`. Similarly, the first occurrence of `A` in the modulus is caused by `A * 2**140`, so we have `d = 140`.
2. Remark that `2**(a+d) = 2**191`. This is a lone `1` that overlaps with `A * 2**188`! In other words, the chunk `10111101` that we saw previously is caused by `2**(a+d) + A * 2**188` (this confirms we're definitely on the right track). From this we also learn that `e = 188`.
3. We can also derive that `1000011001` is caused by `A * 2**512 + B * 2**511`. So we got `c = 511` and `f = 512`
3. Finally looking at some lone `1`'s we get `b = 477`.

The factorization becomes:

```python
>>> print "p:", (2**a + 2**b + 2**c + A)
6703903965361517118576511528025622717463828698514771456694902115718276634989944955753407851598489976727952425488221391817052769267904281935379659980013749
>>> print "q:", (2**d + 2**e + 2**f + B)
13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903820008890319855427587165500997237443558735689450602365103
>>> print "Factorized:", p*q == modulus
True
```

## Generating Private Key and Decrypting

Using [`rsatool.py`](https://github.com/ius/rsatool/blob/master/rsatool.py) we generate a private key from `p` and `q`:

```bash
$ ./rsatool.py -p 6703903965361517118576511528025622717463828698514771456694902115718276634989944955753407851598489976727952425488221391817052769267904281935379659980013749 -q 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903820008890319855427587165500997237443558735689450602365103 -o private.pem
[...]
Saving PEM as private.pem
$ cat private.pem
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAIA
CAAAAAIAAAAAAAAIAAAAAAEMgAAAFeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAA
C9AAAAAAC1AAAAAAAAAAAAAFeAAAAAB7uwIDAQABAoGAah4V4gSlm1pkpZtaZKWbWmSlm1pkpZta
ZKWbWmSlm1pkpZtaZKWbWmtHfLiE7/ux7E4VWmSlm1pkrD07wsQ+GR2F4owloppdZaKaXWWiml1l
oppdZaKaXWWiml1loppdZaMEe3uEhIU5R4a4eVDaXWWiml1loppdaiShi151BvkCQQCAAAAAIAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAC1
AkEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAABAAAAAAAAAA
AAAAAAAAAAAArwJACpD1bw01MsrNNTLKzTUyys01MsrNNTLKzTUyys01MsrNNTLKzTUyys01MsrN
NTLKzTUyys01MsrNNdvaJCXb6QJBAP0TAuz9EwLs/RMC7P0TAuz9EwLs/RMC7P0TAuz9EwLs/RMC
7P0TAu0M5DMbzORC7P0TAuz9EwLs/RMC7P0TA5kCQEQP2f/yE0zeS2vDoF/vHP3qD8MFnj5oY0oN
TsXoUTHUqa87BFWkOP0My4pc8UIResigL/QWrpOjNRAf8YRAzp4=
-----END RSA PRIVATE KEY-----
```

And we decrypt `flag.enc`, which contains a base64 encoded string, using the following python script:

```python
def decrypt_RSA(private_key_loc, package):
    from Crypto.PublicKey import RSA 
    from Crypto.Cipher import PKCS1_OAEP 
    from base64 import b64decode 
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    decrypted = rsakey.decrypt(b64decode(package)) 
    return decrypted
flag = "eItbvkj78nP6H1H5M1vE9HIJwP/yNuSHsLUQyiEsvISZkQsdHvHa6TUgMNcn11QRrkKaLoDIjyBxTRMi+eTJA27ojvpmfTTRUmWn1f8Yo+yBrnaUTEDKf911R4c614SwvMOdv2wQjRDnVQ2s5nxSvW8q3/FzTOgBaWDkp0Qko54="
print decrypt_RSA('private.pem', flag)
```

Let's run this:

```bash
$ python decrypt.py 
We setup private server somewhere, can you find the url of it: ASIS_md5(url)
```

## Oh hell naw?! RECON?!?!

So we have to find the URL of a **private** server which is located **somewhere**. In this case a **private** server means a hidden Tor service/server. The URL we have to find is a `.onion` address. [The Tor documentation](https://trac.torproject.org/projects/tor/wiki/doc/HiddenServiceNames) explains how such addresses are generated:

> If you decide to run a hidden service Tor generates an ​RSA-1024 keypair. The .onion name is computed as follows: first the ​**SHA1 hash of the ​DER-encoded ​ASN.1 public key** is calculated. Afterwards the **first half of the hash is encoded to ​Base32** and the suffix ".onion" is added. Therefore .onion names can only contain the digits 2-7 and the letters a-z and are exactly 16 characters long.

Let's calculate the `.onion` address for our public/private key combination and the resulting flag:

```bash
$ openssl rsa -in private.pem -pubout -outform DER |python -c 'import sys,hashlib,base64;\
print base64.b32encode(hashlib.sha1(sys.stdin.read()[22:]).digest()[:10]).lower()'
writing RSA key
2ekrevuoueus267z
$ echo -n "2ekrevuoueus267z.onion" | md5sum
f4fa90d969aab09c660a774303d7cd77
```

So the URL is `2ekrevuoueus267z.onion` which gives the flag:

    ASIS_f4fa90d969aab09c660a774303d7cd77

I hate RECON challenges so much.

## Other write-ups and resources

* none yet
