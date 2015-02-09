# HITCON CTF 2014: mid

**Category:** ACM
**Points:** 250
**Description:**

> Problem A
>
> http://54.64.29.164:32384/

**Hint:**

> gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1)
> gcc -O2 -static source.c
> Read input from stdin and write output to stdout.
> Single test case in each file, but test several times on multiple file.
>
> It's a CTF challange, you may need a interesting trick to solve it.
> Both setrlimit & cgroup is used.
> (memory.limit_in_bytes, memory.swappiness, RLIMIT_AS)
>
> No temp file is allowed. In fact, it's chroot to an read-only empty directory.
> No socket, IPC, so you can't send the test data out.
> Number of process limit to 8.
> All syscall is allowed.
>
> You need to STEAL MORE MEMORY, but how? where?

## Write-up

(TODO)

## Other write-ups and resources

* <http://puu.sh/aXd9p/44f33626e7.txt>
