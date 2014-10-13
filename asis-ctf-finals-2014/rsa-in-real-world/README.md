# ASIS Cyber Security Contest Finals 2014: RSA in real world!

**Category:** Crypto, Recon
**Points:** 250
**Description:**

> Download [file](rsa_20bdc0fc3b3b06f7a5f920abb4dddfca) and capture the flags!!!

## Write-up

Let’s see what [the provided file](rsa_20bdc0fc3b3b06f7a5f920abb4dddfca) could be:

```bash
$ file rsa_20bdc0fc3b3b06f7a5f920abb4dddfca
rsa_20bdc0fc3b3b06f7a5f920abb4dddfca: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < rsa_20bdc0fc3b3b06f7a5f920abb4dddfca > rsa`
* `unxz < rsa_20bdc0fc3b3b06f7a5f920abb4dddfca > rsa`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x rsa_20bdc0fc3b3b06f7a5f920abb4dddfca
```

Let’s find out what the extracted file is:

```bash
$ file rsa
rsa: gzip compressed data, from Unix, last modified: Sun Oct 12 12:02:01 2014
```

The rabbit hole goes deeper…

```bash
$ gunzip < rsa > rsa-unzipped

$ file rsa-unzipped
rsa-unzipped: POSIX tar archive

$ tar vxf rsa-unzipped
x RSA/
x RSA/flag.enc
x RSA/pubkey.pem
```

(TODO)

## Other write-ups

* none yet
