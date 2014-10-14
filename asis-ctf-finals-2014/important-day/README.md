# ASIS Cyber Security Contest Finals 2014: Important day!

**Category:** Forensics
**Points:** 100
**Description:**

> When did the computer start? Download this [file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa)
>
> `flag = ASIS_md5(time), time = ~$ date +%Y:%m:%d:%H:%M`

## Write-up

### Analyzing the provided file

Let’s see what [the provided file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa) could be:

```bash
$ file impday_92fe19a8b4b2ad415e9d8e1e6aba67aa
impday_92fe19a8b4b2ad415e9d8e1e6aba67aa: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < impday_92fe19a8b4b2ad415e9d8e1e6aba67aa > impday`
* `unxz < impday_92fe19a8b4b2ad415e9d8e1e6aba67aa > impday`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x impday_92fe19a8b4b2ad415e9d8e1e6aba67aa
```

Let’s find out what the extracted file is:

```bash
$ file impday
impday: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 1514)
```

### Brute forcing the flag

From the [ASIS Quals 2014](https://github.com/ctfs/write-ups/tree/master/asis-ctf-quals-2014#readme) we remembered that checking a flag was done on the client side, in JavaScript. The flag submission page contained a hidden field called `id_check` which was used to check the flag:

```js
if (sha256(sha256(flag)) == id_check) {
  // flag is correct
}
```

A quick look at the flag submission code tells us the same mechanism is used for this CTF. This is interesting, because it gives us the power to brute force flags locally.

The challenge suggests we needed a date in the format `+%Y:%m:%d:%H:%M`. This means we don’t care about seconds, which makes the date rather easy to brute force.

Using Wireshark we found that the first packet in the provided packet capture file had timestamp `1412157562`, so the system must’ve been started some time before that.

We brute forced the flag using the following script:

```python
#!/usr/bin/env python
# coding=utf-8

import datetime
import hashlib

def check_flag(flag):
  hash1 = hashlib.sha256(flag)
  hex1 = hash1.hexdigest()
  hash2 = hashlib.sha256(hex1)
  hex2 = hash2.hexdigest()

  return hex2 == '5ed2645dfc6752f1b105c422d07dcd73807758d259c5783c10bea8b0426b77df'

time = 1412157562
flag_found = False

while not flag_found:
  time -= 60
  time_str = datetime.datetime.fromtimestamp(time).strftime('%Y:%m:%d:%H:%M')
  md5hash = hashlib.md5(time_str)
  md5hex = md5hash.hexdigest()
  flag = 'ASIS_%s' % md5hex
  if check_flag(flag):
    print flag
    flag_found = True
```

After a couple of seconds this printed out the flag: `ASIS_d6f98bae92a83f10ca6c488c4612e8fc`.

## Other write-ups and resources

* none yet
