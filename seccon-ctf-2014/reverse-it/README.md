# SECCON CTF 2014: Reverse it

**Category:** Binary
**Points:** 100
**Description:**

> [`Reverseit`](Reverseit)

## Write-up

Let’s take the challenge name literally and reverse the hexadecimal representation of the bytes in the file:

```bash
$ xxd -p Reverseit | tr -d '\n' | rev | xxd -r -p > reversed

$ file reversed
reversed: JPEG image data, JFIF standard 1.01
```

The result is a JPEG image that displays a horizontally flipped (“reversed”) version of the flag:

![](reversed.jpg)

The flag is `SECCON{6in_tex7}`.

## Other write-ups and resources

* none yet
