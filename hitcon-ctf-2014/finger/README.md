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

This one was fairly easy to do but that's because of a programming error, the challenge was supposed to be ginger (which was added later during the ctf-event)? Nevertheless let's get started:
If we study the ruby code which was given to us we can see that we have to play some kind of rock-paper-scissors against the "boss". Of course to make it more difficult, the boss hits for 10-50 dmg while you do only 1-3 dmg. You both have a hp pool of 100. The program expects a magic input which will be compared to the MD5 hash of your secret (the hand you'll be playing) so you just choose a hand and send the MD5 hash of it as the magic word. After you say the magic word, the program says which hand the boss will play so you can compare it to your own hand. Now because of a programming error you can give the program a secret (your hand) which wasn't the one you choose in the beginning. The program will say you're a cheater but you'll only receive 1 dmg (much better than the 10-50 dmg from the boss in the case you would loose). Thus it is only a matter of writing a little script which formats the input and decides to either cheat or win/draw the rock-paper-scissor. 
The netto win rate of this method is something of a 1 dmg per turn so you'll eventually win.
The flag is `HITCON{you are super lucky OAQ!}`.


## Other write-ups

* none yet
