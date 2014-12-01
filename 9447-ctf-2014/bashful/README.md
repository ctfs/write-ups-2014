# 9447 CTF 2014: bashful

**Category:** Web
**Points:** 101
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

## Other write-ups and resources

* none yet
