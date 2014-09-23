# CSAW CTF 2014: Obscurity

**Category:** Forensics
**Points:** 200
**Description:**

> see or do not see
>
> Written by marc
>
> [pdf.pdf](pdf.pdf)

## Write-up

[The provided PDF file](pdf.pdf) contains some hidden text.

One way to get to it is by opening the PDF in your viewer of choice, selecting all of its contents (using `Ctrl` + `A` or `⌘` + `A`), copying it, and then pasting it into your text editor of choice.

Another possible solution is to use the `pdftotext` command-line utility:

```bash
$ pdftotext pdf.pdf

$ strings pdf.txt
flag{security_through_obscurity}
```

The flag is `security_through_obscurity`.

## Other write-ups

* https://hackucf.org/blog/csaw-2014-forensics-200-obscurity/
* http://shankaraman.wordpress.com/2014/09/22/csaw-ctf-2014-forensics-200-obscurity-writeup/
