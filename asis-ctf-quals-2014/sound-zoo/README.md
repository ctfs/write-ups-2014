# ASIS Cyber Security Contest Quals 2014: Sound Zoo

**Category:** Stego
**Points:** 150
**Description:**

> [file](steg_150_e3cdf499ed8341fe750530b93b6ff816)

## Write-up

Let’s see what [the provided file](steg_150_e3cdf499ed8341fe750530b93b6ff816) could be:

```bash
$ file steg_150_e3cdf499ed8341fe750530b93b6ff816
steg_150_e3cdf499ed8341fe750530b93b6ff816: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < steg_150_e3cdf499ed8341fe750530b93b6ff816 > stego_150`
* `unxz < steg_150_e3cdf499ed8341fe750530b93b6ff816 > stego_150`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x steg_150_e3cdf499ed8341fe750530b93b6ff816
```

Let’s find out what the extracted file is:

```bash
$ file stego_150
stego_150: POSIX tar archive
```

Extract the tar archive:

```bash
$ tar -vxzf stego_150
x steg_150_ccf8db5e8cf287469ed291212577f032
```

And inspect the extracted file:

```bash
$ file steg_150_ccf8db5e8cf287469ed291212577f032
steg_150_ccf8db5e8cf287469ed291212577f032: Audio file with ID3 version 2.3.0, contains: MPEG ADTS, layer III, v1, 192 kbps, 44.1 kHz, JntStereo
```

Okay, so it’s an MP3 file that seems to contain a series of engine sounds followed by a computer voice. The computer voice seems to be slowed down though. Open the file in Audacity, go to Effect → Tempo and increase the tempo to 1100% to hear the computer voice reading a code:

```
bbe60b482d22ea98a4d0ef205f772a8b
```

Since the CTF rules state that each flag is of the format `ASIS_x` where `x` is an MD5 hash unless explicitly stated otherwise, the flag is `ASIS_bbe60b482d22ea98a4d0ef205f772a8b`.

## Other write-ups and resources

* [Persian](http://xploit.ir/asis-2014-quals-%D8%A8%D8%A7%D8%BA-%D9%88%D8%AD%D8%B4-%D8%B5%D8%AF%D8%A7/)
