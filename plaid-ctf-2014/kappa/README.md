# Plaid CTF 2014: kappa

**Category:** Pwnables
**Points:** 275
**Description:**

> There's got to be a way to get into [this service](kappa-f2fdf7fcc074cb0c66c3d80a48286450.tar.bz2) set up by the Plague at 54.80.112.128:1313. Can you find it?

## Write-up

(TODO)

```bash
$ nc 54.80.112.128 1313
Thank you for helping test CTF plays Pokemon! Keep in mind that this is currently in alpha which means that we will only support one person playing at a time. You will be provided with several options once the game begins, as well as several hidden options for those true CTF Plays Pokemon fans ;). We hope to expand this in the coming months to include even more features!  Enjoy! :)
Choose an Option:
1. Go into the Grass
2. Heal your Pokemon
3. Inpect your Pokemon
4. Release a Pokemon
5. Change Pokemon artwork
```

```
11:30:24 <saelo> since I couldn't find a writeup, how was kappa supposed to be solved?
11:30:43 <saelo> I got eip control but couldn't really find anything for NX bypass...
11:34:25 <saelo> couldn't find something for stack pivoting + no mmap or similar in plt
11:51:08 <Reinhart> saelo: we constructed an infoleak, found address of system() using that, then set the print_info callback for a pokemon to system(). then make sure the pokemon's name is a shell cmd.
11:51:39 <saelo> Reinhart: cool, that was my idea too, what did you use for the info leak?
11:52:26 <Reinhart> saelo: the attack name was a pointer-to-pointer-to-string, we overwrote it with a pointer to within another pokemon's artwork, then we could change that artwork to leak data up to the next null byte by printing the pokemon
```

## Other write-ups and resources

* <https://blog.skullsecurity.org/2014/plaidctf-writeup-for-pwn-275-kappa-type-confusion-vuln>
* <http://eindbazen.net/2014/04/plaidctf-2014-kappa-275/>
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/pwnables/kappa)
* <http://j00ru.vexillium.org/dump/ctf/kappa.py>
* <http://pastebin.com/VUKdnkLz>
