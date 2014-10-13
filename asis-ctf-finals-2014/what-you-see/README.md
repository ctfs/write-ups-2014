# ASIS Cyber Security Contest Finals 2014: What you see?

**Category:** Stego
**Points:** 175
**Description:**

> Download the [file](milad_eb1ac478beffbbd33c564fbe6396042f).

## Write-up

Let’s see what [the provided file](milad_eb1ac478beffbbd33c564fbe6396042f) could be:

```bash
$ file milad_eb1ac478beffbbd33c564fbe6396042f
milad_eb1ac478beffbbd33c564fbe6396042f: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < milad_eb1ac478beffbbd33c564fbe6396042f > milad`
* `unxz < milad_eb1ac478beffbbd33c564fbe6396042f > milad`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x milad_eb1ac478beffbbd33c564fbe6396042f
```

Let’s find out what the extracted file is:

```bash
$ file milad
milad: PNG image data, 1200 x 800, 8-bit/color RGB, non-interlaced
```

(TODO)

## Other write-ups

* none yet
