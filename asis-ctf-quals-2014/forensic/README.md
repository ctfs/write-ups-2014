# ASIS Cyber Security Contest Quals 2014: forensic

**Category:** Forensic
**Points:** 150
**Description:**

> [file](forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3)

## Write-up

Let’s see what [the provided file](forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3) could be:

```bash
$ file forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3
forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3 > forensic_150`
* `unxz < forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3 > forensic_150`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3
```

Let’s find out what the extracted file is:

```bash
$ file forensic_150
forensic_150: POSIX tar archive
```

Extract the tar archive:

```bash
$ tar -vxzf forensic_150
x forensic_150_2ca7d28df77ec506efc36dd09a146b13
```

And inspect the extracted file:

```bash
$ file forensic_150_2ca7d28df77ec506efc36dd09a146b13
forensic_150_2ca7d28df77ec506efc36dd09a146b13: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 65535)
```

This is a pcap file. Let’s open it in Wireshark and fire up a packet search for the string “flag” in the packet bytes. All results seem to be comments to some HTML/JavaScript code about a boolean variable (a flag) — except for one result, which seems to be the result of a file download called `myfile`. Extracting this file from the pcap and using the Linux `file` command we see that `myfile` is actually another pcap file. However, loading it in Wireshark doesn’t seem to work — the file is broken. We ran `pcapfix` on `myfile` which succesfully repaired it so it could be opened in Wireshark. Investigating this file reveals a file upload to an HP device, most likely a printer. Again, we extract this file which resulted in a PostScript file that contained the flag in ASCII art.

## Other write-ups and resources

* <http://blog.squareroots.de/en/2014/05/asis-ctf-2014-forensic/>
* <http://tasteless.eu/2014/05/asis2014-forensic-150-forensic/>
* <http://blog.dul.ac/2014/05/ASISCTF14/>
* <http://singularityctf.blogspot.de/2014/05/asis-ctf-quals-2014-writeup-forensic.html>
