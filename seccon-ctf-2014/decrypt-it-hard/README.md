# SECCON CTF 2014: Decrypt it (Hard)

**Category:** Crypto
**Points:** 300
**Description:**

> ```
> g^k=69219086192344
> 20<k<20000
> ```
>
> [`c2.zip`](c2.zip)

## Write-up

(TODO)

```bash
$ unzip c2.zip
Archive:  c2.zip
   creating: crypt2/
  inflating: crypt2/E
  inflating: crypt2/eflag.bin
  inflating: crypt2/readme.txt

$ cat crypt2/readme.txt
./E 1 69219086192344 flag.png eflag.bin

$ file crypt2/E
crypt2/E: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, stripped
```

## Other write-ups and resources

* none yet
