# ASIS Cyber Security Contest Finals 2014: Secure hobby

**Category:** Pwn
**Points:** 250
**Description:**

> [File](hobby_8524ad2ae5fde9a43d7e6b1956c8099b) is running here:
>
> ```bash
> nc asis-ctf.ir 12439
> ```

## Write-up

Let’s see what [the provided file](hobby_8524ad2ae5fde9a43d7e6b1956c8099b) could be:

```bash
$ file hobby_8524ad2ae5fde9a43d7e6b1956c8099b
hobby_8524ad2ae5fde9a43d7e6b1956c8099b: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < hobby_8524ad2ae5fde9a43d7e6b1956c8099b > hobby`
* `unxz < hobby_8524ad2ae5fde9a43d7e6b1956c8099b > hobby`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x hobby_8524ad2ae5fde9a43d7e6b1956c8099b
```

Let’s find out what the extracted file is:

```bash
$ file hobby
hobby: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped
```

(TODO)

## Other write-ups

* none yet
