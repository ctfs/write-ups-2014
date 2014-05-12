# ASIS Cyber Security Contest Quals 2014: Tortureous sound

**Category:** Trivia, Stego
**Points:** 75
**Description:**

> Listen to the attached file and find the flag
> [file](stego_75_5ecb5b98aa04033a9855416daed603c8)

## Write-up

Let’s see what [the provided file](stego_75_5ecb5b98aa04033a9855416daed603c8) could be:

```bash
$ file stego_75_5ecb5b98aa04033a9855416daed603c8
stego_75_5ecb5b98aa04033a9855416daed603c8: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < stego_75_5ecb5b98aa04033a9855416daed603c8 > stego_75`
* `unxz < stego_75_5ecb5b98aa04033a9855416daed603c8 > stego_75`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x stego_75_5ecb5b98aa04033a9855416daed603c8
```

Let’s find out what the extracted file is:

```bash
$ file stego_75
stego_75: POSIX tar archive (GNU)
```

Okay, let’s extract the tar archive:

```bash
$ tar -xvf stego_75
x stego_75_111cbfefb1af0175b73d8800ba187ebc
```

…and figure out what the extracted file is:

```bash
$ file stego_75_111cbfefb1af0175b73d8800ba187ebc
stego_75_111cbfefb1af0175b73d8800ba187ebc: ISO Media, MPEG v4 system, version 2
```

Opening the file in Audacity reveals that it is indeed an audio file with 6 channels.

(TODO)

## Other write-ups

* http://blog.squareroots.de/en/2014/05/asis-ctf-2014-tortureous-sound/
