# ASIS Cyber Security Contest Finals 2014: XORQR

**Category:** PPC
**Points:** 150
**Description:**

> Connect here and find the flag:
>
> ```bash
> nc asis-ctf.ir 12431
> ```

## Write-up

_This write-up is made by Steven of the [HacknamStyle](http://hacknamstyle.net/) CTF team._

This challenge sends, after you send "START", a blob of text consisting of "-" and "+"
characters formatted in a square, such as this one:

```
-+++++-+---++-+-----+
-------++--++-+++++++
--+++--++--++-++---++
--+++--++--++-++---++
--+++--++-----++---++
-------++++---+++++++
-+++++-++-----+-----+
+-----++---+---+++++-
+-+--+--+--+-+-------
-+++-++-++--+--+++--+
-+++-+-++++-+--+++++-
+--++-++--++++-+--+--
++--++--+--+++-++-++-
+-----+++-+-+-++++---
-+++++-++--+++---++-+
-------++-++++-+++++-
--+++--+--++-------++
--+++--+---++++++-++-
--+++--+++-++++++-+-+
-------+--+++-+-+--++
-+++++-+--++++-++-+-+
```

This blob represents a QR code where each character represents either a white or
black pixel. The QR code is mangled so that some rows and columns have been inverted.
With information from wikipedia about [QR codes](http://en.wikipedia.org/wiki/QR_code)
we can see that the QR code can be restored by making sure that the Position
and Alignment patterns are shown correctly.
After that, it's just a matter of decoding the restored QR code and submitting
the decoded text. After 15 rounds or so, where the server sometimes injects "?"
instead of "-" or "+", which automatically gets repaired, we get the flag.

```
Congratulations! The flag is ASIS_68d47fab03368ff94025a4f4a1dabf0f
```

The script to solve this challenge is in ```solve-xorqr.py```, and 15 QR codes
received and restored from the server are in ```example-qrs```.

## Other write-ups and resources

* <https://github.com/arkty/asis-ctf-finals-2014-xorqr>
* <http://blog.squareroots.de/en/2014/10/asis-finals-2014-xoror-ppc-150/>
