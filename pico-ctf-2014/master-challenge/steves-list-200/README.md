# Pico CTF 2014 : Steves List 

**Category:** Master Challenge
**Points:** 200
**Description:**

>This program is obviously broken, but thanks to ASLR, PIE, and NX it's still pretty secure! Right?
NB: This problem is running in a slightly unusual setup to get extra PIE randomness. If you have an exploit that works 100% reliably locally (outside of GDB, which often disables any randomness), but you can't get it to land on our server, feel free to message us for help. [Source](hardcore_rop.c) [Binary](hardcore_rop)

>nc vuln2014.picoctf.com 4000

**Hint:**
>This is a statically linked binary (using musl libc). There is no full libc available for you to return into, but if you can leak a .text section address you can return into main(), randop(), and the chunks of libc that are included. Also, you'll probably need to hunt for ROP gadgets: here is a nice tool for that.

>[shell-storm.org](http://shell-storm.org/project/ROPgadget/)

## Write-up

(TODO)

## Other write-ups and resources

* <http://ehsandev.com/pico2014/web_exploitation/steves_list.html>
* <https://ctf-team.vulnhub.com/picoctf-2014-steves-list/>
