# Pico CTF 2014 : Tyrannousaurus Hex

**Category:** Miscellaneous
**Points:** 10
**Description:**

>The contents of the flash drive appear to be password protected. On the back of the flash drive, you see the hexadecimal number 0x95f48ed9 scribbled in ink. The password prompt, however, only accepts decimal numbers. What number should you enter? (Press the Hint button for advice on solving the challenge)

**Hint:**
>You could try asking [Google](https://www.google.com/) or [Wolfram Alpha](http://www.wolframalpha.com/).

## Write-up

We have to convert the hexadecimal number `0x95f48ed9` to decimal and can do that by using `printf`:

```bash
$ printf "%d\n" 0x95f48ed9
2515832537
```

The flag is `2515832537`.

## Other write-ups and resources

* <https://picoctf.wordpress.com/2014/11/10/tyrannosaurus-hex-10-picoctf-2014-writeup/>
* <http://ehsandev.com/pico2014/miscellaneous/tyrannosaurus_hex.html>
