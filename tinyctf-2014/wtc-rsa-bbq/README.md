# tinyCTF 2014: WTC RSA BBQ

**Category:** Crypto
**Points:** 200
**Description:**

> [Download file](cry200.zip)

## Write-up

Let’s extract [the provided `cry200.zip` file](cry200.zip):

```bash
$ unzip cry200.zip
Archive:  cry200.zip
  inflating: cry200
```

The extracted `cry200` file is another ZIP file:

```bash
$ file cry200
cry200: Zip archive data, at least v2.0 to extract
```

So let’s extract it as well:

```bash
$ unzip cry200
Archive:  cry200
  inflating: cipher.bin
  inflating: key.pem
```

(TODO)

## Other write-ups

* none yet
