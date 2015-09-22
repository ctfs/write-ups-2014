# Ghost in the Shellcode 2014: Rabbit of Caerbannog

**Category:** Choose your Pwn Adventure 2
**Points:** 75
**Description:**

> Challenge available from within PwnAdventure2.

## Write-up

The challenge was to defeat a seemingly invincible rabbit.

Reading the code reveals that it can only be killed using a _Holy Hand Grenade_, an item that can only be traded for _89 gears_. Unfortunately, there is no legitimate way to get _gears_.

However, you can get them by triggering an integer overflow. Try to buy 999,999,999 Holy Hand Grenades at once, and this will give you lots of grenades and lots of gears, too.

The flag is `Thy_foe_b31ng_n4ughty_1n_My_s1ght_shall_snuff_it`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/01/ghost-in-shellcode-2014-pwn-adventure-2.html>
* <http://tasteless.eu/2014/01/gits-2014-rabbit-of-caerbannog-pwn-adventure-75/>
