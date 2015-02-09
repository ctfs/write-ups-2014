# Ghost in the Shellcode 2014: Moon Boots

**Category:** Choose your Pwn Adventure 2
**Points:** 50
**Description:**

> Challenge available from within PwnAdventure2.

## Write-up

The challenge was to enter the Moon level somehow.

This can be done in several ways:

1. by hacking the gravity modifier, changing it from `-9.81` to, say, `0.5`
2. by hacking the initial jump velocity modifier, changing it to a value higher than `25`

That way, it’s possible to jump out of bounds on the regular map, which effectively teleports you to the moon.

The flag is `Use a Tab, Space will leave you breathless`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/01/ghost-in-shellcode-2014-pwn-adventure-2.html>
