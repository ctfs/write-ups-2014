# 9447 CTF 2014: johnlions

**Category:** Exploitation
**Points:** 250
**Solves:** 28
**Description:**

> telnet johnlions.9447.plumbing
> login ctf
>
> **Hint!** If you’re not familiar with UNIX, check out <http://www.lemis.com/grog/Documentation/Lions/book.pdf> :P
>
> **Hint!** With a million ways to get root, remember some are much simpler than others…

## Write-up

```bash
$ telnet johnlions.9447.plumbing
Trying 54.148.182.249...
Connected to johnlions.9447.plumbing.
Escape character is '^]'.
login: ctf
$ ls -lsa
total 134
   1 drwxrwxr-x 9 root      272 Sep 22 06:38 .
   1 drwxrwxr-x 9 root      272 Sep 22 06:38 ..
   5 drwxrwxr-x 2 bin      2512 Sep 22 06:38 bin
  18 -rwxr-xr-x 1 bin      8986 Jun  8  1979 boot
   1 drwxrwxr-x 2 bin       208 Sep 22 05:56 dev
   1 drwxrwxr-x 2 bin       336 Sep 22 06:24 etc
   1 -r-------- 1 root       28 Sep 22 06:25 flag
   1 drwxrwxr-x 2 bin       320 Sep 22 05:33 lib
   1 drwxrwxr-x 2 root       96 Sep 22 05:46 mdec
   1 drwxrwxrwx 2 root      112 Sep 22 06:36 tmpc
 102 -rwxr-xr-x 1 root    51982 Jun  8  1979 uniax
   1 drwxrwxr-x12 root      208 Sep 22 05:58 ustr
```

## Other write-ups and resources

* [Write-up by hypnosec](https://github.com/hypnosec/writeups/blob/master/2014/9447-ctf/exploitation/johnlions.md)
* <https://github.com/rick2600/writeups/blob/master/9447CTF_2014/johnlions.md>
* [Write-up + exploit by Ricky Zhou](https://rzhou.org/~ricky/9447_2014/johnlions/)
* <https://github.com/pwning/public-writeup/blob/master/9447ctf2014/exploitation/johnlions/johnlions.md>
