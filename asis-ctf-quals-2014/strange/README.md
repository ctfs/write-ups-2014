# ASIS Cyber Security Contest Quals 2014: Censored array

**Category:** Crypto, PPC
**Points:** 1
**Description:**

> ```bash
> nc 87.107.123.4 9301
> ```

## Write-up

```
$ file crypto_100_0846ec09aab1276d3f58132e9e0d9040
crypto_100_0846ec09aab1276d3f58132e9e0d9040: xz compressed data
$ tar xJvf crypto_100_0846ec09aab1276d3f58132e9e0d9040
x 1c2a7ff1d5cdf3d36544551ae18e30c8
$ file 1c2a7ff1d5cdf3d36544551ae18e30c8
1c2a7ff1d5cdf3d36544551ae18e30c8: ASCII text, with very long lines
$ cat 1c2a7ff1d5cdf3d36544551ae18e30c8
193783664954325860839119335839123899215102615420822972351760578005089136540425309354036361893838393003588891746622376179640815659427394332341396349623915618698881917748452642227703372088122750038977875271898725946720852004880885256474153240496403679762658175476439747881512983568010339887513815290532457778339653199840844995620334862083972129131373571189257219076954184188287439143813927696901842427070726653570329826784994939781399262722041373098152896420678252225833798975089624831218241591628711120707329895543671411906901315360684109949162093034473760905475852393975531277897806950327343042645059549958465853312789713887760614613019996408541328573908373854848160937603498857471516627134163969286531049737140365371424114198553258003189099111625628658195048410056477354418943486633764457994737288416245326617781808808365823018019007303548026276450867096742624996960312090440565297914562234479315177247633875823205403409920418528411649247750473506398553163169161650499998659753179520467576895466482641387252430718673195843748651606278144
```
So we've got a big integer, let's convert it to hex and save it as a file.
```
$ python bignum2hex.py ./1c2a7ff1d5cdf3d36544551ae18e30c8
$ file out.hex
out.hex: 7-zip archive data, version 0.3
$ xxd -l16 out.hex
0000000: 377a bcaf 271c 0003 b73b 9b2c 3f01 0000  7z..'....;.,?...
```

Note the [header/file signature](http://www.garykessler.net/library/file_sigs.html) for a 7z compressed file: `377A BCAF 271C`. Let's extract it.

```
$ 7z e out.hex
7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
p7zip Version 9.20 (locale=utf8,Utf16=on,HugeFiles=on,8 CPUs)

Processing archive: out.hex

Extracting  strange

Everything is Ok

Size:       354
Compressed: 431
$ file strange
strange: lzop compressed data - version 1.030, LZO1X-999, os: Unix
```

Another compression algorithmn, [LZO](http://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Oberhumer). Let's extract it again.

```
$ lzop -dvN strange
decompressing strange into strange.uu
$ file strange.uu
strange.uu: uuencoded or xxencoded text
```

This CTF realy likes to compress, encode and archive. This time, it's [UUEncoding](http://en.wikipedia.org/wiki/Uuencoding). Let's decode it.

```
$ uudecode strange.uu 
$ file strange.U
strange.U: ASCII text
$ cat strange.U
fe18be6a597ffad862b3e8acf9afacb6b6a781efa67acb1a81efad85ab7e
ca8bbe85abdefa7a2dfac79e9fe6de7e8adeffeb617be7e56a0fa2b3e012
212fae9dd7abb1ca2b7bee1bf38d79d5fd7bfb4774ef6db8fbde7b79af1e
6be79ae1a7f4
```

Looks like a hexdump. Let's convert this hexdump to binary.

```
$ xxd -r -p strange.U > strange.bin
$ file strange.bin
strange.bin: data
$ xxd -l16 strange.bin
0000000: fe18 be6a 597f fad8 62b3 e8ac f9af acb6  ...jY...b.......
```

We can't find any header/file signature that matches these first bytes of `strange.bin`. Let's encode it, maybe we get lucky.

```
$ base64 -i strange.bin -o strange.bin.b64
$ file strange.bin.b64
strange.bin.b64: ASCII text
$ cat strange.bin.b64
/hi+all/+this+is+a+strange+message+that+you+have+not+seen+before/+the+flag+is+ASIS+underscore+4b84151f17+0d07224+957ea8ea+ea4af0
```

We had luck. As the original writeup states, the last character of the flag `ASIS\_4b84151f170d07224957ea8eaea4af0` is missing and had to be reconstructed. Read more [here](http://blogs.univ-poitiers.fr/e-laize/2014/05/11/asis-2014-strange/).

## Other write-ups and resources

* <http://blogs.univ-poitiers.fr/e-laize/2014/05/11/asis-2014-strange/>