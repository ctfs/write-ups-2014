# ASIS Cyber Security Contest Finals 2014: Stop!

**Category:** Stego, Crypto
**Points:** 150
**Description:**

> In this [file](stop_53e41e604422d4fa824490ca852dfecb), flag is hidden, find it! and don't stop!

## Write-up

Let’s see what [the provided file](stop_53e41e604422d4fa824490ca852dfecb) could be:

```bash
$ file stop_53e41e604422d4fa824490ca852dfecb
stop_53e41e604422d4fa824490ca852dfecb: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < stop_53e41e604422d4fa824490ca852dfecb > stop`
* `unxz < stop_53e41e604422d4fa824490ca852dfecb > stop`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x stop_53e41e604422d4fa824490ca852dfecb
```

Let’s find out what the extracted file is:

```bash
$ file stop
stop: MPEG sequence, v2, program multiplex
```

Renaming the file to `stop.mpeg` allows us to open it in our video player of choice.

(TODO)

## Other write-ups

* none yet
