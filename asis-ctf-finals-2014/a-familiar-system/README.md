# ASIS Cyber Security Contest Finals 2014: A familiar system

**Category:** Crypto
**Points:** 200
**Description:**

> The flag is encrypted by this [code](crsh_716c88fb8dcc3914b5b5711afecb318e), can you decrypt it after finding the system?

## Write-up

Let’s see what [the provided file](crsh_716c88fb8dcc3914b5b5711afecb318e) could be:

```bash
$ file crsh_716c88fb8dcc3914b5b5711afecb318e
crsh_716c88fb8dcc3914b5b5711afecb318e: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < crsh_716c88fb8dcc3914b5b5711afecb318e > crsh`
* `unxz < crsh_716c88fb8dcc3914b5b5711afecb318e > crsh`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x crsh_716c88fb8dcc3914b5b5711afecb318e
```

Let’s find out what the extracted file is:

```bash
$ file crsh
crsh: POSIX tar archive
```

Let’s extract it:

```bash
$ tar xvf crsh
x crsh/: Refusing to overwrite archive
x crsh/crsh.py
x crsh/flag.enc
tar: Error exit delayed from previous errors.
```

(TODO)

## Other write-ups

* none yet
