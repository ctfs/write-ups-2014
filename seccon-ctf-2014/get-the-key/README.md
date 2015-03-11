# SECCON CTF 2014: Get the key

**Category:** Network
**Points:** 100
**Description:**

> [`nw100.pcap`](nw100.pcap)

## Write-up

Let’s open [the provided packet capture file](nw100.pcap) in Wireshark.

In frame 21 (`frame.number == 21`) a request is made to `http://133.242.224.21:6809/nw100/` using Basic Authentication, with username `seccon2014` and password `YourBattleField`. Let’s re-use those credentials to log in:

```bash
$ curl --user 'seccon2014:YourBattleField' 'http://133.242.224.21:6809/nw100/''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /nw100</title>
 </head>
 <body>
<h1>Index of /nw100</h1>
<table><tr><th><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr><tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[DIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="key.html">key.html</a></td><td align="right">29-Nov-2014 22:12  </td><td align="right"> 48 </td><td>&nbsp;</td></tr>
<tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.2.22 (Debian) Server at 133.242.224.21 Port 6809</address>
</body></html>
```

The page shows a directory listing with a single file named `key.html` in it. Let’s take a look:

```bash
$ curl --user 'seccon2014:YourBattleField' 'http://133.242.224.21:6809/nw100/key.html'
<HTML>
SECCON{Basic_NW_Challenge_Done!}
</HTML>
```

The flag is `SECCON{Basic\_NW\_Challenge\_Done!}`.`

## Other write-ups and resources

* <https://shankaraman.wordpress.com/2014/12/07/seccon-2014-writeups-networking-100-and-programming-100/>
* <http://icheernoom.blogspot.de/2014/12/seccon-ctf-2014-get-key-network-write-up.html>
* [Indonesian](http://www.hasnydes.us/2014/12/get-the-key-seccon-ctf-2014-100pts/)
