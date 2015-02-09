# HITCON CTF 2014: finger

**Category:** Crypto
**Points:** 200
**Description:**

> Are you lucky enough?
> [https://raw.githubusercontent.com/hitcon2014ctf/ctf/master/finger-9312e72601ff37116dd1e201e9508dbb.rb](finger-9312e72601ff37116dd1e201e9508dbb.rb)
> [https://dl.dropbox.com/s/oh5yuu25qj7a8ih/finger-9312e72601ff37116dd1e201e9508dbb.rb](finger-9312e72601ff37116dd1e201e9508dbb.rb)
>
> ```bash
> $ nc 210.71.253.236 7171
> ```

## Write-up

This one was fairly easy to solve because of a programming error in the challenge. An updated harder version of the challenge was released during the CTF under the name of [ginger](https://github.com/ctfs/write-ups/tree/master/hitcon-ctf-2014/ginger).

Studying [the provided Ruby code](finger-9312e72601ff37116dd1e201e9508dbb.rb), we learn that we have to play some kind of rock-paper-scissors against the ‘boss’. To make it more difficult, the boss hits for 10-50 dmg while you do only 1-3 dmg. You both have a HP pool of 100.

The program expects a magic input which will be compared to the MD5 hash of your secret (the hand you’ll be playing). All you have to do is just choose a hand, and send the MD5 hash of it as the magic word. After you send the magic word, the program says which hand the boss plays so you can compare it to your own hand.

Because of a programming error, you can give the program a secret (your hand) which wasn’t the one you choose in the beginning. The program will say you’re a cheater but you’ll only receive 1 dmg, which is much better than the 10-50 dmg from the boss in the case you would loose. Thus it is only a matter of writing [a little script which formats the input and decides to either cheat or win/draw the rock-paper-scissor](solution.rb). The netto win rate of this method is something of a 1 dmg per turn so you’ll eventually win if you run the script for long enough.

The flag is `HITCON{you are super lucky OAQ!}`.

## Other write-ups and resources

* <https://gist.github.com/anonymous/c03c72829af36757eddb>
