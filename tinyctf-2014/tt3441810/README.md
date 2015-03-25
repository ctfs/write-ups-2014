# tinyCTF 2014: tt3441810

**Category:** Reverse Engineering
**Points:** 100
**Description:**

> [Download file](rev100.zip)

## Write-up

Let’s extract [the provided `rev100.zip` file](rev100.zip):

```bash
$ unzip rev100.zip
Archive:  rev100.zip
  inflating: rev100
```

The extracted `rev100` file looks like a hexdump:

```bash
$ file rev100
rev100: ASCII text, with CRLF line terminators

$ cat rev100
00400080  68 66 6C 00 00 48 BF 01  00 00 00 00 00 00 00 48
00400090  8D 34 24 48 BA 02 00 00  00 00 00 00 00 48 B8 01
004000A0  00 00 00 00 00 00 00 0F  05 68 61 67 00 00 48 BF
004000B0  01 00 00 00 00 00 00 00  48 8D 34 24 48 BA 02 00
004000C0  00 00 00 00 00 00 48 B8  01 00 00 00 00 00 00 00
004000D0  0F 05 68 7B 70 00 00 48  BF 01 00 00 00 00 00 00
004000E0  00 48 8D 34 24 48 BA 02  00 00 00 00 00 00 00 48
004000F0  B8 01 00 00 00 00 00 00  00 0F 05 68 6F 70 00 00
00400100  48 BF 01 00 00 00 00 00  00 00 48 8D 34 24 48 BA
00400110  02 00 00 00 00 00 00 00  48 B8 01 00 00 00 00 00
00400120  00 00 0F 05 68 70 6F 00  00 48 BF 01 00 00 00 00
00400130  00 00 00 48 8D 34 24 48  BA 02 00 00 00 00 00 00
00400140  00 48 B8 01 00 00 00 00  00 00 00 0F 05 68 70 72
00400150  00 00 48 BF 01 00 00 00  00 00 00 00 48 8D 34 24
00400160  48 BA 02 00 00 00 00 00  00 00 48 B8 01 00 00 00
00400170  00 00 00 00 0F 05 68 65  74 00 00 48 BF 01 00 00
00400180  00 00 00 00 00 48 8D 34  24 48 BA 02 00 00 00 00
00400190  00 00 00 48 B8 01 00 00  00 00 00 00 00 0F 05 68
004001A0  7D 0A 00 00 48 BF 01 00  00 00 00 00 00 00 48 8D
004001B0  34 24 48 BA 02 00 00 00  00 00 00 00 48 B8 01 00
004001C0  00 00 00 00 00 00 0F 05  48 31 FF 48 B8 3C 00 00
004001D0  00 00 00 00 00 0F 05
```

Let’s restore it back to its original form using `xxd`:

```bash
$ xxd -r -p rev100
@�hflH�H@��4$H�H�@�hagH�@�H�4$H�@�H�@�h{pH�@�H�4$H�H@�hop@H�H�4$H�@H�@ hpoH�@0H�4$H�@@H�hpr@PH�H�4$@`H�H�@phetH�@�H�4$H�@�H�h@�}
H�H�@�4$H�H�@�H1�H�<@�
```

Hmm, most of it is garbage, but there are ASCII characters that match the expected flag format `flag{…}` in there as well. Looking more closely, it seems like there are occurrences of `h` followed by two characters that are part of the flag. After some fiddling we end up with this script:

```bash
$ sed "s/  / /g" rev100 | xxd -r | strings -n 1 | grep '^h' | cut -c 2- | tr -d '\n'
flag{poppopret}
```

The flag is `flag{poppopret}`.

## Other write-ups and resources

* <https://poerhiza.github.io/ctf/2014/10/05/tinyCTF-write_ups-tt3441810/>
* <https://github.com/evanowe/TinyCTF2014-writeups/blob/master/README.md#tt3441810>
* <https://gist.github.com/balidani/9022f29dce228c9cd296>
* <https://github.com/jesstess/tinyctf/blob/master/tt3441810/tt3441810.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/>
