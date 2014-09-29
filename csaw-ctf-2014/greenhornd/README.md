# CSAW CTF 2014: greenhornd

**Category:** Exploitation
**Points:** 400
**Description:**

> ```bash
> nc 54.164.253.42 9998
> ```
>
> This is one of those "key" challenges we talked about on the stream. Also, you should just CreateFile and WriteFile to stdout for your shellcode. Anything more complicated is probably blocked by the App Container.
>
> Update: You can use AppJailLauncher to launch `greenhornd.exe` just like the game server does with:
>
> ```
> AppJailLauncher.exe /network /key:key /port:9998 /timeout:30 greenhornd.exe
> ```
>
> Written by RyanWithZombies
>
> [greenhornd.exe](greenhornd.exe)
> [AppJailLauncher.exe](AppJailLauncher.exe)

## Write-up

(TODO)

## Other write-ups and resources

* <https://hackucf.org/blog/csaw-2014-exploitation-400-greenhornd-exe/>
* <https://gist.github.com/g05u/221b61d13804c5fd87d0>
