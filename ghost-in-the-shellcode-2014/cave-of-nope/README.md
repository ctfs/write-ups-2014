# Ghost in the Shellcode 2014: Cave of Nope

**Category:** Choose your Pwn Adventure 2
**Points:** 50
**Description:**

> Challenge available from within PwnAdventure2.

## Write-up

The challenge was to enter the area called ‘Creepy Cave’, bridge a huge gap somehow, and then defeat the Spider Queen.

Crossing the gap can only be done after hacking the game files and increasing the player’s running speed or the jump velocity, for example.

To avoid getting killed by the Spider Queen, you could hack the _Wine_ item modifier, so that drinking wine makes you invulnerable (instead of just slightly boosting your damage resistance).

The flag is `At least it wasnt full of Creepers`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/01/ghost-in-shellcode-2014-pwn-adventure-2.html>
