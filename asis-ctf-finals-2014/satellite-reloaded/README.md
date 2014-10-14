# ASIS Cyber Security Contest Finals 2014: Satellite reloaded

**Category:** Reverse
**Points:** 250
**Description:**

> Download [this](2satreloaded_465509d872885f2a92656e29d3881ad6) file and find the flag.

## Write-up

Let’s see what [the provided file](2satreloaded_465509d872885f2a92656e29d3881ad6) could be:

```bash
$ file 2satreloaded_465509d872885f2a92656e29d3881ad6
2satreloaded_465509d872885f2a92656e29d3881ad6: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < 2satreloaded_465509d872885f2a92656e29d3881ad6 > sat`
* `unxz < 2satreloaded_465509d872885f2a92656e29d3881ad6 > sat`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x 2satreloaded_465509d872885f2a92656e29d3881ad6
```

Let’s find out what the extracted file is:

```bash
$ file sat
sat: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.26, stripped
```

(TODO)

## Other write-ups and resources

* none yet
