# CSAW CTF 2014: why not sftp?

**Category:** Forensics
**Points:** 200
**Description:**

> well seriously, why not?
>
> Written by marc
>
> [traffic-5.pcap](traffic-5.pcap)

## Write-up

Open [the provided `traffic-5.pcap` file](traffic-5.pcap) in Wireshark.

There are various ways to look for interesting packets:

1. Go to _Statistics_ → _Conversations_ and look for interesting traffic patterns. Or, alternatively…

2. Go to _Edit_ → _Find Packet_ → _String_ → _Search in packet bytes_, and enter `flag`. Or, alternatively…

3. The challenge name hints at FTP usage, so let’s filter the packet captures over the FTP-DATA protocol by typing `ftp-data` into the filter box. Click the capture labeled number `413`.

Right-click the capture and select _Follow TCP Stream_. Notice how the first few bytes match the file header for ZIP files (`PK\x03\x04`).

To extract this ZIP file from the PCAP file, click the `Save As` button at the bottom, and save it somewhere as a `*.zip` file. Unzip the file however you want and open the `flag.png` inside. It displays:

```
flag{91e02cd2b8621d0c05197f645668c5c4}
```

The flag is `91e02cd2b8621d0c05197f645668c5c4` (which, by the way, happens to be the MD5 hash of the string `network`).

## Other write-ups

* <http://www.mrt-prodz.com/blog/view/2014/09/csaw-ctf-quals-2014---why-not-sftp-200pts-writeup>
* <http://shankaraman.wordpress.com/2014/09/22/csaw-ctf-2014-forensics-200-why-not-sftp-writeup>
