# ASIS Cyber Security Contest Finals 2014: TicTac

**Category:** Forensics
**Points:** 200
**Description:**

> Find flag in [this](tictac_4c56077190984fde63900b3ba14d11dd) file

## Write-up

Let’s see what [the provided file](tictac_4c56077190984fde63900b3ba14d11dd) could be:

```bash
$ file tictac_4c56077190984fde63900b3ba14d11dd
tictac_4c56077190984fde63900b3ba14d11dd: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < tictac_4c56077190984fde63900b3ba14d11dd > tictac`
* `unxz < tictac_4c56077190984fde63900b3ba14d11dd > tictac`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x tictac_4c56077190984fde63900b3ba14d11dd
```

Let’s find out what the extracted file is:

```bash
$ file tictac
tictac: data
```

However, `tictac` seems to be a packet capture file.

(TODO)

## Other write-ups

* <http://www.mrt-prodz.com/blog/view/2014/10/asis-ctf-finals-2014---tictac-200pts-writeup>
