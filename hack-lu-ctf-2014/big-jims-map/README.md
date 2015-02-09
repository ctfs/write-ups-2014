# Hack.lu CTF 2014: Big Jim’s Map

**Category:** Reversing
**Points:** 400
**Author:** r1cky
**Description:**

> On the hunt for gold we came across a guy called Big Jim, he is supposed to have one of the biggest treasures. One of your friends from the saloon has special skills when it comes to recon, so he was willing to follow the guy around. He found out that the guy is running a backup server which has a map (flag) to his treasure, but the only way to access the server is through a minimal http server, which allows you to request files, but nothing more. The service is backdoored somehow, which allows Jim to gain full access.
>
> We managed to retrieve a copy of the service binary, as well as a copy of the original one.
> Your job is to reverse the binary, find the backdoor and gain access to system to retreive the map (flag). Good luck.
>
> Service running at: `nc wildwildweb.fluxfingers.net 1406`
>
> kernel:
> - Linux bigjim 3.13.0-37-generic #64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014 x86_64 GNU/Linux
>
> libs:
> - libc-2.19.so (7b6bbcea6627deace906d80edaefc631)
> - libgcc.so (811b3fc49164d5e9bff7d8ba28c960f0)
> - libstdc++.so.6.0.19 (d57085f9589bad60675e16bdfe2f402e)
>
> download: [files](bigjim_8fecca5dc6569e0668b6e48388ddbd1a.tar.gz)


## Write-up

(TODO)

## Other write-ups and resources

* [Write-up by @jhector](https://github.com/jhector/big-jims-map)
