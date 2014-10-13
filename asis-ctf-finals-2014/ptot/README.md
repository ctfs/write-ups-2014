# ASIS Cyber Security Contest Finals 2014: PTOT

**Category:** Stego, Crypto
**Points:** 150
**Description:**

> Find flag in the [image](PTOT_1d23c8694e5cf6727b9ed21285a0d61f)!
>
> **Hint:** You can see that:
>
> `1 --> 3`
>
> and so on…

## Write-up

Let’s see what [the provided file](PTOT_1d23c8694e5cf6727b9ed21285a0d61f) could be:

```bash
$ file PTOT_1d23c8694e5cf6727b9ed21285a0d61f
PTOT_1d23c8694e5cf6727b9ed21285a0d61f: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < PTOT_1d23c8694e5cf6727b9ed21285a0d61f > ptot`
* `unxz < PTOT_1d23c8694e5cf6727b9ed21285a0d61f > ptot`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x PTOT_1d23c8694e5cf6727b9ed21285a0d61f
```

Let’s find out what the extracted file is:

```bash
$ file ptot
ptot: JPEG image data, JFIF standard 1.01
```

The image contains the ‘Periodic Table of Typefaces’ of which you can find [a PDF version online](http://www.voiceonapage.com/ProjectsTypography/Typeface%20Poster/PTOT.pdf).

(TODO)

## Other write-ups

* none yet
