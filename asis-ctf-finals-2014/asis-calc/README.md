# ASIS Cyber Security Contest Finals 2014: ASIS calc

**Category:** Reverse
**Points:** 250
**Description:**

> Download the [file](ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb) and find the flag.

## Write-up

Let’s see what [the provided file](ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb) could be:

```bash
$ file ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb
ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb > calc`
* `unxz < ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb > calc`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x ASIScalc_c4b96a8c1eb9d0881f0c599456d0fceb
```

Let’s find out what the extracted file is:

```bash
$ file calc
calc: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, stripped
```

(TODO)

## Other write-ups and resources

* none yet
