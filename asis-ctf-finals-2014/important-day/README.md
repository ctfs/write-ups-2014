# ASIS Cyber Security Contest Finals 2014: Important day!

**Category:** Forensics
**Points:** 100
**Description:**

> When did the computer start? Download this [file](impday_92fe19a8b4b2ad415e9d8e1e6aba67aa)
>
> `flag = ASIS_md5(time), time = ~$ date +%Y:%m:%d:%H:%M`

## Write-up

### Analyzing the provided file

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

### Intended solution

Let’s open this up with Wireshark. This capture file contains a lot of TCP `SYN` packets sent from `192.168.100.5` to `192.168.100.78`. All of these packets are answered with an `ACK/RST` packet, meaning that the port is closed. This looks like a capture from a `SYN` portscan.

Most `SYN`s are denied, except for a few (`tcp.stream eq 2007`). These packets contain extra information, namely the `TSval` and `TSecr` properties.

According to [RFC 1323](http://tools.ietf.org/html/rfc1323), the `TSval` should be “at least approximately proportional to real time”. That means if we can find the scaling value, we can calculate when the `TSval` was `0`. Although `TSval` can be chosen at random at startup, it would make sense that it was set to `0` when the server was started. (How else could we solve this puzzle?)

| ID     | `TSval`      | Time(s)      | Diff(s) Time | Diff (`TSval`) |
|--------|--------------|--------------|--------------|----------------|
| 1      | `2400803286` | `178.174412` | `0`          |  `0`           |
| 2      | `2400803326` | `178.335906` | `0.161494`   |  `40`          |

From this, we can calculate how many `TSval` ticks there are per second. The `TSval` increases with `40` over a time period of `0.167494` seconds, so there is an increase of about `250` ticks per second. (Using the real value creates an error that doesn’t lead to the solution. This is only one sample and a value of `250` ticks per second seems logical.) The `TSval` value for the first packet is `2400803286`. That means that the server started `2400803286 / 250 ~= 9603213.144` seconds ago.

The Epoch time for the first packet is `1412157739.276447000`, so the server should have started at `1402554526.132447`. This corresponds with `Thu, 12 Jun 2014 06:28:46 GMT`. The resulting MD5 hash appears to be incorrect. Since the server is probably located in Iran, we may have to use the Iranian timezone, which is UTC+4.30. The final time is therefore `2014:06:12:10:58`. This gives us `ASIS_{MD5(2014:06:12:10:58)}`, or `ASIS_d6f98bae92a83f10ca6c488c4612e8fc`, which is the solution.

### Alternate solution using brute force

From the [ASIS Quals 2014](https://github.com/ctfs/write-ups/tree/master/asis-ctf-quals-2014#readme) we remembered that checking a flag was done on the client side, in JavaScript. The flag submission page contained a hidden field called `id_check` which was used to check the flag:

```js
if (sha256(sha256(flag)) == id_check) {
  // flag is correct
}
```

A quick look at the flag submission code tells us the same mechanism is used for this CTF. This is interesting, because it gives us the power to brute force flags locally.

The challenge suggests we needed a date in the format `+%Y:%m:%d:%H:%M`. This means we don’t care about seconds, which makes the date rather easy to brute force.

Using Wireshark we found that the first packet in the provided packet capture file had timestamp `1412157562`, so the system must’ve been started some time before that.

We brute forced the flag using the following script:

```python
#!/usr/bin/env python
# coding=utf-8

import datetime
import hashlib

def check_flag(flag):
  hash1 = hashlib.sha256(flag)
  hex1 = hash1.hexdigest()
  hash2 = hashlib.sha256(hex1)
  hex2 = hash2.hexdigest()

  return hex2 == '5ed2645dfc6752f1b105c422d07dcd73807758d259c5783c10bea8b0426b77df'

time = 1412157562
flag_found = False

while not flag_found:
  time -= 60
  time_str = datetime.datetime.fromtimestamp(time).strftime('%Y:%m:%d:%H:%M')
  md5hash = hashlib.md5(time_str)
  md5hex = md5hash.hexdigest()
  flag = 'ASIS_%s' % md5hex
  if check_flag(flag):
    print flag
    flag_found = True
```

After a couple of seconds this printed out the flag: `ASIS_d6f98bae92a83f10ca6c488c4612e8fc`.

## Other write-ups and resources

* <http://beagleharrier.wordpress.com/2014/10/14/asis-ctf-finals-2014important-day-writeup/>
