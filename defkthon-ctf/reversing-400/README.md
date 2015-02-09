# DEFKTHON CTF: Reversing 400

**Description:**

> [BIN](400.bin)

## Write-up

_This write-up is made by the [HacknamStyle](http://hacknamstyle.net/) CTF team._

Running `file 400.bin` gives no useful information: it only detects data. Similarly, `strings 400.bin` also provides no useful information. Executing `binwalk 400.bin` to extract possible hidden files reveals a Squashfs filesystem with a DD-WRT signature:

```bash
$ binwalk 400.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             LZMA compressed data, properties: 0x6D, dictionary size: 8388608 bytes, uncompressed size: 2709328 bytes
851968        0xD0000         Squashfs filesystem, big endian, DD-WRT signature, version 3.0, size: 2787244 bytes,  676 inodes, blocksize: 131072 bytes, created: Sat Jan 11 14:04:28 2014
```

So we’re dealing with a DD-WRT firmware image.

Using [the Firmware Modification Kit](https://code.google.com/p/firmware-mod-kit/) and executing `extract-firmware.sh 400.bin` successfully extracts the filesystem. Now the question is how and where the flag is hidden:

1. Is a special password configured somewhere? `grep -ri pass .`, nope.
2. Is a flag in plaintext hidden somewhere? `grep -ri flag .`, YES!

In the file `rootfs/etc/www` we encountered the line `</html>'flag is caputdraconis`. Hence the flag to solve this level is `caputdraconis`.

## Other write-ups and resources

* none yet
