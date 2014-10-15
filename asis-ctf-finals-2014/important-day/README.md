# ASIS Cyber Security Contest Finals 2014: Important day!

**Category:** Forensics
**Points:** 100
**Description:**

> When did the computer start? Download this [file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa)
>
> `flag = ASIS_md5(time), time = ~$ date +%Y:%m:%d:%H:%M`

## Write-up

Let’s see what [the provided file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa) could be:

```bash
$ file impday_92fe19a8b4b2ad415e9d8e1e6aba67aa
impday_92fe19a8b4b2ad415e9d8e1e6aba67aa: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < impday_92fe19a8b4b2ad415e9d8e1e6aba67aa > impday`
* `unxz < impday_92fe19a8b4b2ad415e9d8e1e6aba67aa > impday`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x impday_92fe19a8b4b2ad415e9d8e1e6aba67aa
```

Let’s find out what the extracted file is:

```bash
$ file impday
impday: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 1514)
```
So let's open this up with WireShark.

This capture file contains a lot of TCP `SYN` packets sent from `192.168.100.5` to `192.168.100.78`. All of these packets are answered with an `ACK/RST` packet, meaning that the port is closed. This looks like a capture from a SYN portscan.

Most SYN's are denied, except for a few (`tcp.stream eq 2007`). These packets contain extra information: `TSval` and `TSecr`.

According to [RFC1323](http://tools.ietf.org/html/rfc1323), the TSval should "at least approximately proportional to real time". That means if we can find the scaling value, we can calculate when the TSval was 0. Although TSval can be chosen at random at startup, it would make sense that it was set to 0 when the server was started. (How else can we solve this puzzle?)
nr	TSval			Time(s)			Diff(s) (Time)	Diff (TSval)
1	2400803286		178.174412		0				0
2	2400803326		178.335906		0.161494		40


From this, we can calculate how many TSval ticks there are per second. TSval increases with 40 over a time period of 0.167494 seconds, so there is an increase of (about) 250 ticks in 1 second. (Using the real value creates an error that doesn't lead to the solution. This is only one sample and a value of 250 ticks per second seems logical.) The TSval value for the first packet is 2400803286. That means that the server started `2400803286 / 250 ~= 9603213,144` seconds ago. 

The epoch time for the first packet is `1412157739,276447000 seconds`, so the server should have started at `1402554526,132447 seconds`. This corresponds with `Thu, 12 Jun 2014 06:28:46 GMT`. The resulting md5 appears to be incorrect. Since the server is probably located in Iran, we may have to use the Iranian timezone, which is UTC+4.30. The final time is therefore 2014:06:12:10:58. This gives us ASIS_MD5(2014:06:12:10:58) = ASIS_d6f98bae92a83f10ca6c488c4612e8fc, which is the solution.

## Other write-ups and resources

* <http://beagleharrier.wordpress.com/2014/10/14/asis-ctf-finals-2014important-day-writeup/>
