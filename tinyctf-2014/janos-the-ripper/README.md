# tinyCTF 2014: János the Ripper

**Category:** Miscellaneous
**Points:** 100
**Description:**

> [Download file](misc100.zip)

## Write-up

Let’s extract the provided `misc100.zip` file:

```bash
$ unzip misc100.zip
Archive:  misc100.zip
  inflating: misc100
```

The extracted `misc100` file is another ZIP archive:

```bash
$ file misc100
misc100: Zip archive data, at least v2.0 to extract
```

Let’s try to unzip it:

```bash
$ unzip misc100
Archive:  misc100
[misc100] flag.txt password:
password incorrect--reenter:
   skipping: flag.txt                incorrect password
```

Oh, it’s password-protected! Let’s crack the password usig `fcrackzip` or, as the challenge name suggests, `john`:

```bash
$ zip2john misc100 > zip-hashes
/tmp/misc100->flag.txt PKZIP Encr: cmplen=39, decmplen=25, crc=7788D444

$ cat zip-hashes
/tmp/misc100:$pkzip$1*1*2*0*27*19*7788d444*0*26*8*27*7788*0010014b93ff03ee9cfad31283a15788578cbf41aa418716f685fe4002da73ca1fac169789443a*$/pkzip$

$ john zip-hashes --show
/tmp/misc100:fish

1 password hash cracked, 0 left
```

A-ha! The ZIP password is `fish`. Now we can unzip the archive:

```bash
$ unzip -P 'fish' misc100
Archive:  misc100
  inflating: flag.txt
```

The extracted `flag.txt` file contains the flag:

```
flag{ev3n::y0u::bru7us?!}
```

## Other write-ups and resources

* <http://sugarstack.io/tinyctf-misc-100.html>
* <https://github.com/evanowe/TinyCTF2014-writeups/blob/master/README.md#j%C3%A1nos-the-ripper>
* <https://github.com/jesstess/tinyctf/blob/master/janos/janos.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/>
