# SECCON CTF 2014: ROP: Impossible

**Category:** Exploit
**Points:** 500
**Description:**

> ropi.pwn.seccon.jp:10000
>
> Read `/flag` and write the content to stdout, such as the following pseudo code.
>
> ```
> open("/flag", 0);
> read(3, buf, 32);
> write(1, buf, 32);
> ```
>
> Notice that the `vuln` executable is protected by an Intel Pin tool, the source code of which is `norop.cpp`.
>
> [`vuln`](vuln)
> [`norop.cpp`](norop.cpp)
> [`norop_conf`](norop_conf)

## Write-up

(TODO)

## Other write-ups and resources

* <https://rzhou.org/~ricky/seccon2014/rop_impossible/>
