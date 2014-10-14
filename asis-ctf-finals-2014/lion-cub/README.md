# ASIS Cyber Security Contest Finals 2014: Lion Cub

**Category:** Reverse Engineering
**Points:** 100
**Description:**

> Flag is encrypted using this [program](simple_f0455e55c1d236a28387d04d5a8672ad), can you find it?

## Write-up

Let’s see what [the provided file](simple_f0455e55c1d236a28387d04d5a8672ad) could be:

```bash
$ file simple_f0455e55c1d236a28387d04d5a8672ad
simple_f0455e55c1d236a28387d04d5a8672ad: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < simple_f0455e55c1d236a28387d04d5a8672ad > lion-cub`
* `unxz < simple_f0455e55c1d236a28387d04d5a8672ad > lion-cub`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x simple_f0455e55c1d236a28387d04d5a8672ad
```

Let’s find out what the extracted file is:

```bash
$ file lion-cub
lion-cub: gzip compressed data, from Unix, last modified: Sat Oct 11 11:44:23 2014
```

The ASIS CTF organizers sure like compressing files…

```bash
$ gunzip < lion-cub > lion-cub-unzipped

$ file lion-cub-unzipped
lion-cub-unzipped: POSIX tar archive (GNU)

$ tar xvf lion-cub-unzipped
x simple/
x simple/simple_5c4d29f0e7eeefd7c770a22a93a1daa9
x simple/flag.enc
```

(TODO)

## Other write-ups and resources

* none yet
