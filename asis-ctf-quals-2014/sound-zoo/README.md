# ASIS Cyber Security Contest Quals 2014: Sound Zoo

**Category:** Stego
**Points:** 150
**Description:**

> [file](steg_150_e3cdf499ed8341fe750530b93b6ff816)

## Write-up

The file is actually an mp3 file which seems to contain a series of engine sounds followed by a computer voice.  
The computer voice seems to be slowed down though. If we increase the tempo by 1100% with audacity we can hear the computer voice reading a code:
```
bbe60b482d22ea98a4d0ef205f772a8b
```
flag:
```
ASIS_bbe60b482d22ea98a4d0ef205f772a8b
```

## Other write-ups

* none yet
