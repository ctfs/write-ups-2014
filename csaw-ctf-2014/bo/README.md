# CSAW CTF 2014: bo

**Category:** Exploitation
**Points:** 100
**Description:**

> exploit this
>
> ```bash
> nc 54.165.176.104 1515
> ```
>
> Written by HockeyInJune
>
> [bo](bo)

## Write-up

[The provided `bo` file](bo) is an ELF executable:

```bash
$ file bo
bo: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, not stripped
```

This may not be the intended solution, but simply looking for ASCII strings in the binary reveals the flag:

```bash
$ strings bo | grep 'flag'
flag{exploitation_is_easy!}
```

Alternatively, you could open the file in [IDA](https://www.hex-rays.com/products/ida/support/download.shtml) (which is what the challenge actually suggests if you run it) and click _View_ → _Open Subviews_ → _Strings_.

The flag is `exploitation_is_easy!`.

## Other write-ups

* <http://www.mrt-prodz.com/blog/view/2014/09/csaw-ctf-quals-2014---bo-100pts-writeup>
* <http://evandrix.github.io/ctf/2014-csaw-exploitation-100-bo.html>
