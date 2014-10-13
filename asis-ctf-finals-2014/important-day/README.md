# ASIS Cyber Security Contest Finals 2014: Important day!

**Category:** Forensics
**Points:** 100
**Description:**

> When did the computer start? Download this [file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa)
>
> `flag = ASIS_md5(time), time = ~$ date +%Y:%m:%d:%H:%M`

## Write-up

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

(TODO)

## Other write-ups

* none yet
