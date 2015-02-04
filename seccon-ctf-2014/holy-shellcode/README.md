# SECCON CTF 2014: Holy shellcode

**Category:** Exploit
**Points:** 400
**Description:**

> Get the `keyword.txt` from `hebrew.pwn.seccon.jp:10016`.
>
> Holy shellcode using Hebrew characters in UTF-16LE
<http://hebrew.pwn.seccon.jp/nikud/hebrew-utf16le.html>
>
> Server files:
>
> 1. [`stage16`](stage16)
> 2. [`stage16_conf`](stage16_conf)
>
> For example:
>
> ```bash
> $ vi holy.nasm
> BITS 32
> db 0x24,0xFB,0x34,0xFB,0x1E,0xFB,0x1F,0xFB
> db 0x0a
> $ nasm -f bin holy.nasm -o holy
> $ cat holy | nc hebrew.pwn.seccon.jp 10016
> ```
>
> Bless you!

## Write-up

(TODO)

## Other write-ups and resources

* <https://rzhou.org/~ricky/seccon2014/holy_shellcode/>
* <http://pastebin.com/Fau8A3La>
