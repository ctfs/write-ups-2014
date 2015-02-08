# Sharif University Quals CTF 2014: Recover Deleted File

**Category:** Forensics
**Points:** 40
**Solves** 216
**Description:**

> Recover the disk and find the flag.
>
> [Download](disk-image.gz)

## Write-up

First, we extract the given `gzip` compressed file using `gunzip disk-image.gz`, then we find out what type of file the resulting file is:

```bash
$ file disk-image
disk-image: Linux rev 1.0 ext3 filesystem data
```

Using `binwalk`, we see that it contains an ELF that might be interesting:

```bash
$ binwalk disk-image
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Linux EXT filesystem, rev 1.0 ext3 filesystem data, UUID=bc6c2b24-106a-4570-bc4f-ae09abbdabbd
65536         0x10000         Linux EXT filesystem, rev 1.0 ext3 filesystem data, UUID=bc6c2b24-106a-4570-bc4f-ae09abbdabbd
72704         0x11C00         Linux EXT filesystem, rev 1.0 ext3 filesystem data, UUID=bc6c2b24-106a-4570-bc4f-ae09abbdabbd
1113088       0x10FC00        ELF 64-bit LSB executable, AMD x86-64, version 1 (SYSV)
1116896       0x110AE0        LZMA compressed data, properties: 0x89, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
1117024       0x110B60        LZMA compressed data, properties: 0x9A, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
1117216       0x110C20        LZMA compressed data, properties: 0xB6, dictionary size: 16777216 bytes, uncompressed size: 33554432 bytes
1117408       0x110CE0        LZMA compressed data, properties: 0xD8, dictionary size: 16777216 bytes, uncompressed size: 50331648 bytes
```

So we write our own [scalpel config file](scalpel.conf) and extract the elf using `scalpel`:

```bash
$ scalpel -c scalpel.conf disk-image
[...]
$ tree scalpel-output
scalpel-output/
├── audit.txt
└── elf-0-0
    └── 00000000.elf

    1 directory, 2 files
```

So what does this executable do? Let's find out:

```bash
$ chmod u+x ./scalpel-output/elf-0-0/00000000.elf && ./scalpel-output/elf-0-0/00000000.elf
your flag is:
de6838252f95d3b9e803b28df33b4baa
```

Looks like our flag is `de6838252f95d3b9e803b28df33b4baa`.

## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/15/>
