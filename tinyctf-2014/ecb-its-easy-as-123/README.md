# tinyCTF 2014: ECB, it’s easy as 123

**Category:** Crypto
**Points:** 300
**Description:**

> [Download file](cry300.zip)

## Write-up

Let’s extract the provided `cry300.zip` file:

```bash
$ unzip cry300.zip
Archive:  cry300.zip
  inflating: cry300
```

The extracted `cry300` file is another ZIP archive:

```bash
$ file cry300
cry300: Zip archive data, at least v2.0 to extract
```

So let’s unzip it as well:

```bash
$ unzip cry300
Archive:  cry300
  inflating: ecb.bmp
  inflating: task.txt
```

The extracted `task.txt` file says:

> Somebody leaked a still from the upcoming Happy Feet Three movie,
> which will be released in 4K, but Warner Bros. was smart enough
> to encrypt it. But those idiots used a black and white bmp format,
> and that wasn't their biggest mistake. Show 'em who's boss and
> get the flag.

The BMP file is not actually a valid image file because it is encrypted. Its first few bytes are interesting:

```bash
$ hexdump -C ecb.bmp | head -n2
53 61 6c 74 65 64 5f 5f  ab 31 b5 e5 ca 3d b9 4d  |Salted__.1...=.M|
```

The `Salted__` prefix indicates this file is [encrypted using OpenSSL](http://justsolve.archiveteam.org/wiki/OpenSSL_salted_format). The next 8 bytes (`ab 31 b5 e5 ca 3d b9 4d`) are the salt that was used to encrypt the file. The rest of the file is the encrypted data.

TODO: Bruteforce until first two bytes are `BM` (header for BMP)?

$ openssl enc -d -aes-256-ecb -salt -in ecb.bmp -k "$password" | head -c2

## Other write-ups

* none yet
