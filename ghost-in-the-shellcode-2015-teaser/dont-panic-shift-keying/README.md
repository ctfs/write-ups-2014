# Ghost in the Shellcode 2015 teaser: Don’t Panic! Shift Keying!

**Description:**

> Extract the key!
>
> [File](dontpanic-8f27ebde0a2a714871c57e4d9a526b06c86b12212249f984cdb9eefe81bf8f7c)

## Write-up

```bash
$ file dontpanic-8f27ebde0a2a714871c57e4d9a526b06c86b12212249f984cdb9eefe81bf8f7c
dontpanic-8f27ebde0a2a714871c57e4d9a526b06c86b12212249f984cdb9eefe81bf8f7c: bzip2 compressed data, block size = 600k

$ bunzip2 < dontpanic-8f27ebde0a2a714871c57e4d9a526b06c86b12212249f984cdb9eefe81bf8f7c > dontpanic

$ file dontpanic
dontpanic: POSIX tar archive

$ tar xjfv dontpanic
x dontpanicshiftkeying/README
x dontpanicshiftkeying/key.iq
x dontpanicshiftkeying/
x dontpanicshiftkeying/dontpanicshiftkeying.jpg
```

(TODO)

## Other write-ups and resources

* <http://gnoobz.com/gits-teaser-2015-ctf-dont-panic-shift-keying-writeup.html>
* <http://www.clevcode.org/ghost-in-the-shellcode-2015-teaser-dont-panic-shift-keying-solution/>
