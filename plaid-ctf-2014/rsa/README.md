# Plaid CTF 2014: rsa

**Category:** Forensics
**Points:** 450
**Description:**

> Our archaeologists recovered a dusty and corrupted old hard drive used by The Plague in his trips into the past. It contains a private key, but this has long since been lost to bitrot. Can you recover the full key from the [little information we have recovered](rsa-6537e9aae493b0c43601d1dbc2da2ce2.tar.bz2)?

## Write-up

_This write-up is made by Steven of the [HacknamStyle](http://hacknamstyle.net/) CTF team._

After some Googling, a tool can be found to recover corrupted RSA private keys, linked to the paper [_Reconstructing RSA Private Keys from Random Key Bits_ by Nadia Heninger and Hovav Shacham](http://cseweb.ucsd.edu/~hovav/papers/hs09.html).

The `rsabits` tool takes a corrupted private and public key as input, and then recovers the missing bits. To distinguish actual vs. missing bits, `rsabits` uses a ‘mask’ where an ‘on’ bit means ‘known’ and an ‘off’ bit means ‘unknown’. Since this is an academic prototype, the code needs [some patching to actually output the recovered private key](rsabits.patch).

The input file for `rsabits` consists of two parts: the public key information and the private key information.

The modulus and exponent of the public key can be extracted using the following command:

```bash
$ cat public.pub | grep -v -- ----- | tr -d '\n' | base64 -d | openssl asn1parse -inform DER -i -strparse 18
0:d=0  hl=3 l= 137 cons: SEQUENCE
3:d=1  hl=3 l= 129 prim:  INTEGER           :DBFABDB1495D3276E7626B84796E9FC20FA13C1744F10C8C3F3E3C2C6040C2E7F313DFA3D1FE10D1AE577CFEAB7452AA53102EEF7BE0099C022560E57A5C30D50940642D1B097DD2109AE02F2DCFF8198CD5A395FCAC4266107848B9DD63C387D2538E50415343042033EA09C084155E652B0F062340D5D4717A402A9D806A6B
135:d=1  hl=2 l=   3 prim:  INTEGER           :010001
```

The bits of the private key can be extracted from the corrupted file after some text-fiddling and converting the hex values to
decimal using `ibase 16` in `bc`.

The final `rsabits` input file can be found in [`input-numbers.txt`](input-numbers.txt), which is fed to the `rsabits` tool:

```bash
$ ./rsa -i input-numbers.txt
```

The tool will print out values for `P` and `Q`:

```
12643740637395110652894262209502063899047520218436247735878188180335985789877601396069401620713231058940443043891453952791936466967524033214476598572706213
12217494205780318874865198006759446969679921137474855298485716817925925911890415286181103665676748660959871257808447814451048738105000263500773868071134927
```

…which can then be converted into a private key using [`rsatool.py`](https://github.com/ius/rsatool/blob/master/rsatool.py):

```bash
$ ./rsatool.py -p 12643740637395110652894262209502063899047520218436247735878188180335985789877601396069401620713231058940443043891453952791936466967524033214476598572706213 -q 12217494205780318874865198006759446969679921137474855298485716817925925911890415286181103665676748660959871257808447814451048738105000263500773868071134927 -o recovered.key
```

[The resulting key](recovered.key) can then be used to decrypt the given ciphertext:

```bash
$ openssl rsautl -decrypt -in ciphertext -out plaintext -inkey recovered.key
```

…which reveals the flag `crypt0>>>f0rensics3~`.

## Other write-ups and resources

* [Write-up by More Smoked Leet Chicken](http://mslc.ctf.su/wp/plaidctf-2014-rsa-writeup/)
* [Write-up by fail0verflow](https://fail0verflow.com/blog/2014/plaidctf2014-for450-rsa.html)
* [Reconstructing RSA private keys from random key bits](http://cseweb.ucsd.edu/~hovav/papers/hs09.html)
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/forensics/rsa)
* [Indonese](http://blog.rentjong.net/2014/04/plaidctf2014-write-up-rsaforensic450.html)
