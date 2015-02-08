# Sharif University Quals CTF 2014: Guess The Number

**Category:** Reverse
**Points:** 30
**Solves** 316
**Description:**

> Guess the number and find the flag.
>
> [Download](guess.jar)

## Write-up

We just have to decompile the `guess.class` inside the `guess.jar` using a decompiler of your choice.
After that, we get the sourcecode [guess.java](guess.java) and can see that we have to guess `my_number/5`, which is `0x5c214f6c/5 = 1545686892/5 = 309137378`.

So if we use this as input for this program using `java guess 309137378`, we get the flag:

> your flag is: a7b08c546302cc1fd2a4d48bf2bf2ddb

## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/12/>
