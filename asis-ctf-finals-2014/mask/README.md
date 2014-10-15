# ASIS Cyber Security Contest Finals 2014: Mask

**Category:** Crypto, Stego
**Points:** 150
**Description:**

> Flag is hidden in [file](mask_e50b38fc9ba38378c444bd93518e886f), find it!
>
> **Hint:** Numerical representation can be useful.

## Write-up

Let’s see what [the provided file](mask_e50b38fc9ba38378c444bd93518e886f) could be:

```bash
$ file mask_e50b38fc9ba38378c444bd93518e886f
mask_e50b38fc9ba38378c444bd93518e886f: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < mask_e50b38fc9ba38378c444bd93518e886f > mask`
* `unxz < mask_e50b38fc9ba38378c444bd93518e886f > mask`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x mask_e50b38fc9ba38378c444bd93518e886f
```

Let’s find out what the extracted file is:

```bash
$ file mask
mask: data
```

Okay, it’s just a bunch of seemingly random, binary data. Let’s use the hint to try to make sense of it, and convert the byte stream into a number. First we use `hexdump` and `xxd` to view the hexadecimal representation of the file, but nothing really stands out. Let’s represent the file as a decimal number. Since the file is quite big, we write a Python script for this:

```py
import binascii
f = open('mask', 'rb')
byte_stream = f.read()
number = int(binascii.hexlify(byte_stream), 16)

with open('big-ass-int.txt', 'w') as number_file:
  number_file.write(str(number))
```

After running this script, `big-ass-int.txt` contains the number, which consists of 674,209 digits:

```bash
$ wc -c big-ass-int.txt
  674209 big-ass-int.txt
```

The number starts with the following digits:

```bash
$ head -c 40 big-ass-int.txt
1415926535890932384626433832095028841971
```

Those look like [the fractional-part digits of `π`](http://www.wolframalpha.com/input/?i=π)! Let’s get the fractional-part digits of `π` and compare them to this number to see if there’s a difference.

[This page](http://www.exploratorium.edu/pi/pi_archive/Pi10-6.html) lists the first million digits of `π`, which is more than enough for our experiment (we only need 674,209 fractional-part digits). After removing the leading `3.` and whitespace we end up with [this file named `pi.txt`](https://gist.githubusercontent.com/anonymous/c2f71add67dd9a7943ad/raw/f1afa4da5012e93921a0c681419427466494a37e/pi-1000000.txt).

Let’s write a Python script `diff.py` to get the digits from the real `π` that are different in the `big-ass-int.txt` file, and format the resulting number in hex.

```python
#!/usr/bin/env python
# coding=utf-8

real_pi = open('pi.txt', 'r').read()
big_ass_int = open('big-ass-int.txt', 'r').read()

result = ''
for i in range(0, len(big_ass_int)):
  if big_ass_int[i] != real_pi[i]:
    result += real_pi[i]

print '%x' % int(result)
```

Let’s treat the hexadecimal output of the script as a byte stream and save the result as a file named `diff.bin`.

```bash
$ python diff.py > diff

$ xxd -r -p diff > diff.bin

$ file diff.bin
diff.bin: xz compressed data
```

Aha, apparently this is another `xz` archive! Let’s extract it using any of the abovementioned techniques:

```bash
$ unxz < diff.bin > extracted

$ file extracted
extracted: PDF document, version 1.5
```

Opening the extracted file in a PDF viewer reveals the flag: `ASIS_d45491d1ad0b63ae05b0f0238d0c48e8`.

## Other write-ups and resources

* none yet
