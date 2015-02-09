# Olympic CTF 2014: As seen on DEFCON

**Category:** Nopsleigh (Pwn)
**Points:** 10
**Author:** snk
**Description:**

> `EBFE` is to x86 as **____** is to ARM64.

## Write-up

This is a reference to [DEF CON 2006’s trivia challenge](http://nopsr.us/ctf2006prequal/walk-trivia.html#500) which went like this:

> `EBFE` is to x86 as **____** is to PowerPC.

This time we have to find the ARM64 equivalent. Let’s see what kind of instruction `EBFE` is:

```bash
$ echo -ne '\xEB\xFE' | ndisasm -
00000000  EBFE              jmp short 0x0
```

Okay, so `\xEB\xFE` is a `jmp` instruction. ARM doesn’t have `jmp` instructions though — [it uses `b` instructions (branches) instead](http://www.heyrick.co.uk/armwiki/B). Let’s see which opcode `b` maps to:

```bash
$ echo 'b .' | aarch64-linux-gnu-as
$ aarch64-linux-gnu-objdump -d a.out

a.out:     file format elf64-littleaarch64


Disassembly of section .text:

0000000000000000 <.text>:
   0:   14000000        b       0 <.text>
```

So the 32-bit instruction word for `b` is `0x14000000`. Since ARM64 is little-endian, this becomes `00000014`.

The answer is `00000014`.

## Other write-ups and resources

* <http://cybersecurity.cci.fsu.edu/olympic-ctf-2014-writeup/>
* <https://ctftime.org/writeup/927>
* <http://ctfwriteups.blogspot.jp/2014/02/olympic-ctf-2014-nopsleigh-10-as-seen.html>
* [Chinese](http://ddaa.logdown.com/posts/178446-olympic-ctf-2014-10-point-summary)
