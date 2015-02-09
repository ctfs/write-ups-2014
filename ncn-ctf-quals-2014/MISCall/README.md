# NoConName 2014 Quals: MISCall

**Category:** Misc
**Points:** 100
**Description:**

No hints :( just go and get the flag.

## Write-up

(Here's a shorter writeup by the Balalaika crew: <http://ctfcrew.org/writeup/67>)

First let's determine the file type...

```
$ file ctf
ctf: bzip2 compressed data, block size = 900k
```

It's a bzip2 compressed archive, let's decompress it and try again.

```
$ mv ctf ctf.bz2
$ bzip2 -d ctf.bz2
$ file ctf
ctf: POSIX tar archive (GNU)
```

So there's a tar file in it. Let's unpack it.

```
$ mv ctf ctf.tar
$ tar -xf ctf.tar
```

A new directory was created.

```
$ cd ctf
$ ls ctf
flag.txt
```

Can't be that easy, right?

```
$ cat flag.txt
Nothing to see here, moving along...
```

Nope, not so easy ;)

Let's take a closer look...

```
$ ls -a
.  ..  flag.txt  .git
```

Aha! It's a Git repository. This looks better. Let's look at the commit log...

```
$ git log
commit bea99b953bef6cc2f98ab59b10822bc42afe5abc
Author: Linus Torvalds <torvalds@klaava.Helsinki.Fi>
Date:   Thu Jul 24 21:16:59 2014 +0200

    Initial commit
```

Not much to see here, just one commit with the file we've already seen. But the repo is a bit too big to contain only this, there must be something else hidden here. The two obvious locations are the branches and the stash.

```
$ git stash show
 flag.txt |   25 ++++++++++++++++++++++++-
 s.py     |    4 ++++
 2 files changed, 28 insertions(+), 1 deletion(-)
```

Gotcha! Let's recover the files.

```
$ git stash apply
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#	new file:   s.py
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#	modified:   flag.txt
#
```

Now flag.txt has a completely different content, it's the mythical email sent by Linus Torvalds announcing the Linux kernel in comp.os.minix. We can also find a Python script with the following contents:

```
$ cat s.py
#!/usr/bin/env python
from hashlib import sha1
with open("flag.txt", "rb") as fd:
    print "NCN" + sha1(fd.read()).hexdigest()
```

So this just calculates the SHA1 hash from flag.txt. We run it and get the flag:

```
$ ./s.py
NCN4dd992213ae6b76f27d7340f0dde1222888df4d3
```

## Other write-ups and resources

* <http://www.incertia.net/blog/noc0nname-quals-2014-miscall-100/>
* <https://ctfcrew.org/writeup/67>
