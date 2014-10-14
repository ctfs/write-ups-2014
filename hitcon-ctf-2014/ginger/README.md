# HITCON CTF 2014: ginger

**Category:** Crypto
**Points:** 400
**Description:**

> Are you lucky enough?
>
> ```bash
> $ nc 210.71.253.236 7979
> ```
>
> [https://raw.githubusercontent.com/hitcon2014ctf/ctf/master/ginger-350e951738280de084cf87d9070356e6.rb](ginger-350e951738280de084cf87d9070356e6.rb)

## Write-up

This problem is the fixed version of the [finger](https://github.com/ctfs/write-ups/tree/master/hitcon-ctf-2014/finger) problem in this CTF which had a bug that allowed you to win fairly easily.
This is a kind of rock-paper-scissors against the ‘boss’, except in the fixed version you can't get out of the damage if you lose, and the damage against the boss is now 1-2 HP.
This means you have to win on average 66 times in 10 minutes, so you have about 9 seconds per round, which makes this problem quite difficult.

If you compare [the provided Ruby
code](ginger-350e951738280de084cf87d9070356e6.rb) with the code for finger
the basics are the same.  The server provides three five-character strings.
The idea is that you select one, and send a proof of your selection.  The
boss reveals his choice at which point you submit your selection.  The trick
is that for your proof you can choose an arbitrary number of 16-character
hashes whose prefix is your choice and submit that *sum* of those hashes as
your proof.  So if you can find a single number whose sum can be generated
in three ways (one for each prefix) you can always win by chosing the
winning choice after the boss reveals his.

There may be other methods, but the way I approached it is as follows. For
each prefix do the following algorithm:

   * Generate a list of random strings, over which you iterate.

   * Consider the MD5 hash of each entry, specifically the last two hex digits
     (i.e. mod 256).  Pair them off so you generate sums which are multiple of 256.
     So for example pair 0x55 with 0xAB.  This will generate a set of
     strings ending in 00.

   * Repeat this process for this new set, to produce strings ending in four
     zeros.  For each of these there are four MD5 hashes which add up to this
     number.

   * Keep repeating this process to level 16 until you have sets of 65,536
     hashes which add up to number ending in 32 zeros.  By the law of
     averages it will be around 32,000 times 2^128.

The code looks like:

```python
    def insert(self, level, hashsum, hashsumtxt, lst):
        if level == 16:
            if (hashsumtxt, 2**16) not in self.options:
                 lst = self.collapse(lst)
                 self.options[(hashsumtxt, len(lst))] = lst
            return
        n = int(hashsumtxt[-level*2-2:][:2], 16)
        if (256-n) in self.data[level]:
            oldhashsum, oldlst = self.data[level][256-n]
            newhashsum = oldhashsum + hashsum
            newhashsumtxt = "%X" % newhashsum
            self.insert(level+1, newhashsum, newhashsumtxt, (oldlst, lst))
        self.data[level][n] = (hashsum, lst)

    def run(self):
        for s, h in make_hashes(self.prefix):
            self.insert(0, int(h, 16), h, [(s,h)])
            if len(self.options) >= OPTION_COUNT:
                break
        return self.options
```

This is where it gets tricky. Due to random variation you don't always get
very near 32,768*2^128, but something close.  Therefore there is a very real
chance the ranges generated for the three prefixes don't overlap.

You can reduce the spread by repeating the processes a 17th time but then
you run into another problem.  You have to send 131,072 hashes of length 16
which works out to 2MB of data.  Sending this to the server takes time as
does processing it.  During the CTF this took about 8 seconds, which is
essentially the entire budget you have per round.  This also meant writing
it in C wouldn't help.  You have to make it work in 16 rounds, which takes 4
seconds of processing.

This is essentially where I got stuck during the CTF (my team didn't solve
it).  However, after the CTF finished the server remained running, which
allowed me to test a few ideas.

This trick eventually turned out to be to control the combining of the pairs
better.  The above algorithm will tend to magnify random biases during the
generation of the hashes.  Basically, we try to steer the summing of the
pairs by looking at the first 16 bits of the sum.

What you do is that for the first level there is no restriction. After one
addition we halve the allowed range so it has to be between 0x4000 and
0xC000, and do this again for each level, so that after 16 levels there is
only one allowed prefix, 0x8000.  At each level there is only a 25% the sum
will fall outside, so it doesn't have a huge effect on the generation time.
But it does mean that at the end of the algorithm we always get 65,536
hashes which add to the same sum:
0x8000_0000_0000_0000_0000_0000_0000_0000_0000.  It manages this in a bit
under a second on my machine.  Note that you only need to generate around
30,000 hashes to reach this result.  The hash generation is not the limiting
factor here.

The changed code looks like:

```python
        if (256-n) in self.data[level]:
            oldhashsum, oldlst = self.data[level][256-n]
            newhashsum = oldhashsum + hashsum
            t = newhashsum >> (128-16+level+1)               # NEW
            if (-32678) <= (t-32768)<<(level) < (32768):     # NEW
                newhashsumtxt = "%X" % newhashsum
                self.insert(level+1, newhashsum, newhashsumtxt, (oldlst, lst))
```

With this change, a stable internet connection, parallelisation and a dose
of luck, this program won with 10 seconds to spare.  The flag is
`HITCON{shik is a stupid guy -.-}`, presumably a reference to the maker of
the original faulty challenge.

NB I'm truly curious if there is a way to solve this challenge in a way that
requires significantly fewer hashes to be sent.  This feels almost like
brute forcing the problem.  Certainly the really tight 10 minute time limit
where about half the time is spend sending hashes suggests there is a
significantly better way.  Also the server doesn't require all the hashes to
have the same prefix, though it's not clear to me that you can use this in
any way.

## Other write-ups and resources

* none yet
