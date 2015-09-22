# Ghost in the Shellcode 2014: lugkist

**Category:** Trivia
**Points:** 150
**Description:**

> Find the key. [File](https://2014.ghostintheshellcode.com/lugkist-3c99ed66685a73f333dde7cddfe5e9a4fd3651f0)

## Write-up

The headers of the provided `lugkist-3c99ed66685a73f333dde7cddfe5e9a4fd3651f0` file contain `7zXZ`, indicating it’s `xz`-compressed data.

So, extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < lugkist-3c99ed66685a73f333dde7cddfe5e9a4fd3651f0 > lugkist.txt`
* `unxz < lugkist-3c99ed66685a73f333dde7cddfe5e9a4fd3651f0 > lugkist.txt`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x lugkist-3c99ed66685a73f333dde7cddfe5e9a4fd3651f0
```

Then, … (TODO)

The flag is `Power overwhelming? Back in my day cheats did not have spaces.`.

## Other write-ups and resources

* <http://blog.zachorr.com/lugkist/>
* <http://commandlinewani.blogspot.com/2014/01/ghostintheshellcode-write-up-lugkist.html>
* <http://delogrand.blogspot.com/2014/01/ghost-in-shellcode-2014-trivia.html>
* <http://tasteless.eu/2014/01/gits-2014-lugkist-trivia-150>
* <https://systemoverlord.com/blog/2014/01/19/ghost-in-the-shellcode-2014-lugkist/>
* [Chinese](http://ddaa.logdown.com/posts/176382-gits-2014-trivia-150-lugkist)
