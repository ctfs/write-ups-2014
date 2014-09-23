# CSAW CTF 2014: dumpster diving

**Category:** Forensics
**Points:** 100
**Description:**

> dumpsters are cool, but cores are cooler
>
> Written by marc
>
> [firefox.mem.zip](firefox.mem.zip)

## Write-up

```bash
$ file firefox.mem.zip
firefox.mem.zip: Zip archive data, at least v2.0 to extract

$ unzip firefox.mem.zip
Archive:  firefox.mem.zip
  inflating: firefox.mem

$ file firefox.mem
firefox.mem: ELF 64-bit LSB core file x86-64, version 1 (SYSV), SVR4-style, from '/usr/lib/firefox/firefox'

$ strings firefox.mem | grep 'flag{'
ZZZZZZZZflag{cd69b4957f06cd818d7bf3d61980e291}
```

The flag is `cd69b4957f06cd818d7bf3d61980e291` (which, by the way, happens to be the MD5 hash of the string `memory`).

## Other write-ups

* <http://www.mrt-prodz.com/blog/view/2014/09/csaw-ctf-quals-2014---dumpster-diving-100pts-writeup>
* <https://hackucf.org/blog/csaw-2014-forensics-100-dumpster-diving/>
* <http://shankaraman.wordpress.com/2014/09/22/csaw-2014-forensics-100-dumpster-driving-writeup>
