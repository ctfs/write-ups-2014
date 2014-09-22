# CSAW CTF 2014: xorcise

**Category:** Exploitation
**Points:** 500
**Description:**

> ```bash
> nc 128.238.66.227 24001
> ```
>
> Written by raid
>
> [xorcise](xorcise)
> [xorcise.c](xorcise.c)

## Write-up

Let’s compile [the provided `xorcise.c` file](xorcise.c) and run some local tests:

```bash
$ gcc -w xorcise.c -o xorcise-local && ./xorcise-local
           ---------------------------------------
           --            XORCISE 1.1b           --
           --   NOW WITH MORE CRYPTOGRAPHY!!!   --
           ---------------------------------------
Entering main listening loop...
```

Now we can connect to the locally running `xorcise` instance:

```bash
$ nc 127.0.0.1 24001
```

As soon as this command is entered, `xorcise-local` logs:

```
Accepted connection from 127.0.0.1
```

Now we can start entering input in the `nc` window…

(TODO)

## Other write-ups

* <http://solution-36.blogspot.com/2014/09/csaw-2014-exploit-500-writeup-xorcise.html>
* <http://tasteless.se/2014/09/xorcise-csaw-2014-exploiting-500/>
