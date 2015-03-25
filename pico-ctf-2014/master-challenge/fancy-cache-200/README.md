# Pico CTF 2014 : Fancy Cache

**Category:** Master Challenge
**Points:** 200
**Description:**

>Margaret wrote a fancy in-memory cache server. For extra security, she made a custom string structure that keeps strings on the heap. However, it looks like she was a little sloppy with her mallocs and frees. Can you find and exploit a bug to get a shell?

>You can connect to the server at [vuln2014.picoctf.com:4548](http://vuln2014.picoctf.com:4548)

>The following exploit mitigations are enabled on the server:

>ASLR: This means the stack, heap, and libc addresses are randomized. However, the locations of code and data inside the binary is not randomized.

>NX: No memory is every simultaneously writable and executable. This means that you cannot just write shellcode somewhere and get the program to jump to it.

>Here's the info (don't worry about the libc file for now): source code, binary, libc

>P.S. We found a client for the server: client.py

**Hint:**
>Is there any way that the server might try to use a struct string after it has been freed? Perhaps we can put something else in the freed memory. For similarly sized allocations, malloc often returns a recently freed address.

>The offset of memcmp in libc is 0x142870. This is different than what objdump says because libc chooses a different memcmp implementaton depending on what features the processor supports.

## Write-up

(TODO)

## Other write-ups and resources

* <http://cregnec.github.io/blog/2014/11/17/picoctf-2014-writeup.html#fancy-cache>
* <https://ctf-team.vulnhub.com/picoctf-2014-fancy-cache/>
* <http://barrebas.github.io/blog/2014/11/06/picoctf-fancy-cache/>
