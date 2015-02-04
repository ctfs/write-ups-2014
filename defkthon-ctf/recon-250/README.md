# DEFKTHON CTF: Recon 250

**Description:**

> Crack Ajin’s [message](http://pastebin.com/nGvKgY23).
> Only [Ajin Abraham](https://www.google.com/#q=ajin+abraham) can help you!

## Write-up

The message provided in the challenge description is a PGP-encrypted email. Let’s start by downloading it and saving it as [`message.pgp`](message.pgp):

```bash
$ curl 'http://pastebin.com/raw.php?i=nGvKgY23' > message.pgp
```

In order to decrypt the message, we’re gonna need the private key used to encrypt it.

Luckily, the HTML source code of [Ajin’s website](http://opensecurity.in/ajinabraham.com/) has this in it:

```
<!--pastebin DOT com/TYHfKbtt-->
```

This leads to a PGP private key. Let’s download it and save it as [`private.key`](private.key):

```bash
$ curl 'http://pastebin.com/raw.php?i=TYHfKbtt' > private.key
```

Now let’s import the private key and use it to decrypt the message:

```bash
$ gpg --allow-secret-key-import --import private.key
gpg: key 8708771F: secret key imported
gpg: key 8708771F: "xboz <xboz@mailinator.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1

$ gpg --decrypt message.pgp

You need a passphrase to unlock the secret key for
user: "xboz <xboz@mailinator.com>"
4096-bit RSA key, ID 8708771F, created 2014-02-18

Enter passphrase:
```

Too bad; we need the private key’s passphrase before we can decrypt the message. You could bruteforce the passphrase, but there was another way to get it for this challenge. [Ajin’s contact form](http://opensecurity.in/ajinabraham.com/) contains the following HTML:

```html
<p id="mail-failure">Unable to send your email! (--wankoff--)</p>
```

It turns out `wankoff` is the passphrase.

```bash
$ gpg --decrypt message.pgp

You need a passphrase to unlock the secret key for
user: "xboz <xboz@mailinator.com>"
4096-bit RSA key, ID 8708771F, created 2014-02-18

gpg: WARNING: cipher algorithm AES256 not found in recipient preferences
gpg: encrypted with 4096-bit RSA key, ID 8708771F, created 2014-02-18
      "xboz <xboz@mailinator.com>"
flag { Pretty007G00d007Privacy }
```

The flag is `Pretty007G00d007Privacy`.

## Other write-ups and resources

* <http://blog.0xdeffbeef.com/2014/03/defkthon-ctf-2014-crack-ajins-message.html>
