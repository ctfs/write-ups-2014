# ASIS Cyber Security Contest Quals 2014: Prying ears

**Category:** Forensic
**Points:** 175
**Description:**

> [file](forensic_175_1f352928fa34c024c9ab15d102b115ce)

## Write-up

The file is a Pcap-ng (Wireshark) file. Running wiresharks protocol hierarchy on the file reveals a lot of DNS traffic.   
Investigating further we notice that most of this DNS traffic consists out of requests to a domain name with the following format: "[0-9a-f]{14}.asis.io". However, all of them result in a "not found" response.

Looking closer we see that all of the prefixes to ".asis.io" are hex format. The first one being "89504e470d0a1a" which contains a PNG header (8950).

So we extracted all the requests with the "[0-9a-f]{14}.asis.io" format, saved the prefixes to a file and transformed them to a png using:
```
xxd -r -p hex.txt out.png
```
The png file contained the flag.



## Other write-ups

* http://tasteless.se/2014/05/asis2014-forensics-175-prying-ears/
