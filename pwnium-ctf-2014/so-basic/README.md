# Pwnium CTF 2014: So basic

**Category:** Misc
**Points:** 75
**Description:**
> Find the Flag (75 pts) [http://41.231.53.40/Misc75.zip](Misc75.zip)

## Write-up

We are given several (39) files with a md5sum as fiename and two characters, a hex byte, as the content of each file.

If we concat all files and decode it from hex to ascii, we get something that is not quite right:

```bash
$ cat * | sed 's/\\x//g' | xxd -r -p
c{352dc0cf9c7efdf560dbb5ued17we7n2Pe}emi
```

We see an upper case `P` as well as an opening and closing curly brace `{`/`}`, so this might be our flag, just not in the right order.

Though we could theroetically bruteforce the flag, we might have to submit each created flag, so that is not a proper solution.

However, we still have the md5sums as filenames. If we decrypt one or two of these md5sums, e.g. with an [online md5 cracker](md5online.org), we quickly see that these are the numbers in the range `0-39`.

So lets concat the hex bytes in the given order according to the md5sum cleartext:

```bash
$ for i in {0..39}; do cat `echo -n $i | md5` | gsed 's/\\x//g' | xxd -r -p; done
Pwnium{02cef7eeb75fdd9dfc67c0dc1e3e255b}
```

Looks like our flag is `Pwnium{02cef7eeb75fdd9dfc67c0dc1e3e255b}`.

## Other write-ups and resources

* <https://crazybulletctfwriteups.wordpress.com/2014/07/07/pwnium-ctf-2014-so-basic/>
* <http://scrubsec.com/2014/07/06/pwnium-ctf-so-basic-75-pts/>
* <https://ctftime.org/writeup/1159>
* <http://blog.dul.ac/2014/07/PWNIUM14/>
