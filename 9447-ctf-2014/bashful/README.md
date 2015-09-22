# 9447 CTF 2014: bashful

**Category:** Web
**Points:** 101
**Solves:** 157
**Description:**

> You think that was too easy? Well it was actually harder than I thought, so I made it simple again…
>
> [bashful.9447.plumbing](http://bashful.9447.plumbing/)

## Write-up

**Note:** This challenge is an easier version of [the _tumorous_ challenge](https://github.com/ctfs/write-ups/tree/master/9447-ctf-2014/tumorous#readme).

The page at <http://bashful.9447.plumbing/> contains:

> 13/2/2004: I learned how to html, yay!
> 12/4/2004: I learned how to use git, yay!
> 13/4/2004: Hidden my 'repository' so people can't access it. I have a feeling I will need to protect something soon.
> 08/9/2004: Forged a token from the whispering iron. It is very dear to me, I should protect it.
> 10/9/2004: I put my token in a text file to protect it from alien mind readers from planet Zblaargh.
> 10/9/2004: I can't forget my token. What do I do? I should also pack so I'm ready to leave soon.
> 11/9/2004: I panicked and deleted the token. It is the work of evil doers.
> 12/9/2004: My token is lost. My life has no meaning now. I'm going to watch Louie season 4.

The second line hints at Git, so let’s try visiting <http://bashful.9447.plumbing/.git/>. This page contains the directory listing for the `.git` folder. Let’s download it:

```bash
$ wget -r -nH -e html_extension=Off --reject '*.html*' 'http://bashful.9447.plumbing/.git/'
```

Since we only have the `.git` folder but not the actual source files, this is a _bare_ Git repository. Luckily, the source files can be restored:

```bash
$ git checkout -f

$ ls
index.html token

$ cat token
9447{I_JUST_THINK_BITCOIN_WILL_DIE_OUT_SOON}
```

The flag is `9447{I_JUST_THINK_BITCOIN_WILL_DIE_OUT_SOON}`.

### Alternate solution

[`.git/logs/HEAD`](http://bashful.9447.plumbing/.git/logs/HEAD) contains:

````
0000000000000000000000000000000000000000 3c4992205aba2077cbf87fc7cde900fabecd1140 root <root@ip-172-31-10-205.ap-southeast-2.compute.internal> 1412673432 +0000commit (initial): Hurr durr
3c4992205aba2077cbf87fc7cde900fabecd1140 ec972f9af79a09129021a30e7f08099aa2b8a81d John Doe <fsck@you.me> 1412673456 +0000	commit (amend): Hurr durr
ec972f9af79a09129021a30e7f08099aa2b8a81d 0b4d6fe0adf809c4e7b7a0d47132600b68f79fda root <root@ip-172-31-10-205.ap-southeast-2.compute.internal> 1417230572 +0000commit: My precious flag now exists
````

So, someone committed the flag, but they’ve probably deleted it in a later commit. Let’s look at the `.git/objects` directory to see if any commit objects can be found. There don’t seem to be any. The CTF organizers might have [packed](http://git-scm.com/book/en/v2/Git-Internals-Packfiles) the commit objects. Let’s look at `.git/objects/info/packs`:

```
I banish thee, evil mind readers from planet Zblaargh.
```

In the initial version of the challenge we were supposed to find the pack file name on our own by directly entering its URL. Pack file names are of the format `pack-${SHA1}.{pack,idx}` where `${SHA1}` is a hash of the sorted object names to make the resulting filename based on the pack content.

Unfortunately there was no (?) way to find out the object name of the token file without knowing the token itself. Anyhow, no team could solve this challenge at that difficulty level. And that’s why the organizers reduced the complexity from 310 to 101 points and made the directories browseable.

Okay, maybe we can just fetch the pack file from the packs directory. Let’s browse to `.git/objects/pack/`:

````
pack-deff83d57714493c6d317394f3542da8e396f887.idx
pack-deff83d57714493c6d317394f3542da8e396f887.pack
````

Fine, let’s download these files and unpack them. An easy way to do this is explained in [this Stack Overflow answer](http://stackoverflow.com/a/3333428/96656).

After unpacking, `git status` shows:

````
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	deleted:    index.html
	deleted:    token
````

The next part is simple:

````
$ git checkout token

$ cat token
9447{I_JUST_THINK_BITCOIN_WILL_DIE_OUT_SOON}
````

## Other write-ups and resources

* <https://github.com/hypnosec/writeups/blob/master/2014/9447-ctf/web/bashful.md>
* <http://tasteless.eu/2014/12/9447-security-society-ctf-2014-bashful-and-coffee-writeup/>
* <https://ucs.fbi.h-da.de/writeup-9447-bashful/>
