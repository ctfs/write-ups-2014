# Stripe CTF3: level1

## Description

Cryptocurrencies are all the rage these days. Thus, today we’re proud to announce the release of a new one, entitled Gitcoin.

It’s easy to start a new Gitcoin instance: you start with a Git repository containing a `LEDGER.txt` file, which represents the starting balances (denoted in the form `username: <balance>`). You then transact by committing balance updates to the repository. A valid ledger might look like this:

```
Private Gitcoin ledger
==============
siddarth: 52
nelhage: 23
woodrow: 41
ludwig: 151
```

There’s a twist, however: in order to push a new commit, that commit’s SHA1 must be lexicographically less than the value contained in the repository’s `difficulty.txt` file. For instance, a commit in a Gitcoin blockchain with difficulty `00005` might look something like the following:

```diff
commit 00004216ba61aecaafb11135ee43b1674855d6ff7
Author: Alyssa P Hacker <alyssa@example.com>
Date:   Wed Jan 22 14:10:15 2014 -0800

    Give myself a Gitcoin

    nonce: tahf8buC

diff --git a/LEDGER.txt b/LEDGER.txt
index 3890681..41980b2 100644
--- a/LEDGER.txt
+++ b/LEDGER.txt
@@ -7,3 +7,4 @@ andy: 30
 carl: 12
 gdb: 45
 pa: 30
+user-hpbsuozt: 1
```

However, it wouldn’t be valid if `difficulty.txt` contained `00003` or `000001`.

The Git repository’s history thus forms a blockchain with a proof-of-work for each block, just like in Bitcoin. Of > course, unlike Bitcoin, Gitcoin just uses Git and doesn’t require a custom client.

Gitcoins are mined by adding yourself to [the `LEDGER.txt`](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level1/problem/LEDGER.txt) with 1 Gitcoin (or incrementing your entry if already present) in a commit with an allowable SHA1. For simplicity, the ledger is maintained centrally and never rolled back (though, there’s no inherent reason we couldn’t decentralize Gitcoin, since it’s built off of the same foundation as Bitcoin).

To beat the level (and gain 50 points), you need to mine a Gitcoin. You’ll be competing against our own mining bot swarm, so you’ll need to out-compute them. (Note that as soon as one of them mines a Gitcoin, you’ll have to throw out all your work and start your search again from the new base commit.)

You can obtain your personal Gitcoin instance here:

```bash
git clone lvl1-qfrfxagh@stripe-ctf.com:level1
```

Your public username for this level is `user-hpbsuozt`, so a winning commit must add `user-hpbsuozt: 1` to the ledger.

To get you started, we’ve included [a sample miner implementation in your Gitcoin instance](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level1/problem/miner). The miner is far too slow to use in practice though.

We’ll start a new Gitcoin instance every 15 minutes in order to keep history short. You should run `git reset --hard origin/master` when this happens in order to reset your clone’s state.

## Write-up

The bottleneck in the provided [`miner` script](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level1/problem/miner) is the following code, found within a hot loop:

```bash
body="tree $tree
parent $parent
author CTF user <me@example.com> $timestamp +0000
committer CTF user <me@example.com> $timestamp +0000

Give me a Gitcoin

$counter"

# See http://git-scm.com/book/en/Git-Internals-Git-Objects for
# details on Git objects.
sha1=$(git hash-object -t commit --stdin <<< "$body")
```

This code generates a Git commit object and computes its hash. Because a new `git` process is launched for every commit object we want to check, this is pretty slow. The key to solving this challenge is to [re-implement Git’s object hashing](http://git-scm.com/book/en/Git-Internals-Git-Objects#Object-Storage) ourselves.

I ended up rewriting the entire `miner` script in Python — see [`miner.py`](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level1/miner.py). Use it as follows:

```bash
$ ./miner.py lvl1-qfrfxagh@stripe-ctf.com:level1 user-hpbsuozt
Mining…
Mined a Gitcoin! The SHA-1 is:
00000037948a0bc8e05e3f85c3198636362c9f40
HEAD is now at 00000037 Give me a Gitcoin
To lvl1-qfrfxagh@stripe-ctf.com:level1
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'lvl1-qfrfxagh@stripe-ctf.com:level1'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Starting over :(
Mining…
Mined a Gitcoin! The SHA-1 is:
00000068d3ff02e5a12967049697ab532ef2b19b
HEAD is now at 00000068 Give me a Gitcoin
Counting objects: 5, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 398 bytes | 0 bytes/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: ===================
remote:
remote: Congratulations, user-hpbsuozt! You've just earned your first Gitcoin. Your leaderboard score is 50.
remote:
remote:
remote: The bots will stop now. You can run `git clone lvl1-qfrfxagh@stripe-ctf.com:current-round` to go head-to-head against other Gitcoin miners and earn more points.
remote:
remote: ===================
To lvl1-qfrfxagh@stripe-ctf.com:level1
   000000ae..00000068 master -> master
Success :)
```

## Other write-ups or solutions

* <http://abiusx.com/stripe-ctf-v3-writeup/>
* <http://tullo.ch/articles/stripe-ctf-golfing/>
* <http://muehe.org/posts/stripe-ctf-3-writeup/>
* [Gibybo’s write-up](https://news.ycombinator.com/item?id=7180991)
* [Jon Eisen’s write-up](http://blog.joneisen.me/post/75008410654)
* [Evan Priestley’s write-up](http://blog.phacility.com/post/stripe_ctf3/)
* [Samuel Walker’s write-up](http://www.samuelwalker.me.uk/2014/01/stripe-ctf3-write-up/)
* <https://github.com/henrik-muehe/level1>
* <https://github.com/xthexder/stripe-ctf-3.0>
* <https://github.com/kratorius/stripe-ctf3/tree/master/level1>
* <https://github.com/lericson/stripe-ctf3/tree/level1>
* [Solution in Haskell](https://gist.github.com/yanatan16/a4517f4804166855c58a)
* [Solution in C/CUDA](https://github.com/metcalf/ctf3/tree/master/level1)
* [Original problems including a modified test harness that works locally](https://github.com/janosgyerik/stripe-ctf3)
