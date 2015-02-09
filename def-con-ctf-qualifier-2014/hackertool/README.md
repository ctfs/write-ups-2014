# DEF CON CTF Qualifier 2014: hackertool

**Category:** Baby’s First
**Points:** 1
**Description:**

> hey, we need to check that your connection works, torrent this file and md5 it
>
> http://services.2014.shallweplayaga.me/hackertool.torrent\_fe3b8b75e9639d35e8ac1d9809726ee2
>
> KINDA A HINT FOR HACKERTOOL: http://imgur.com/XCtMjJ2

## Write-up

The challenge provided us with a .torrent file and told us to download it and use the md5 checksum of the file inside as flag. I first tried to straight up download the file but it was almost a 60gb download and it seemed to be throttled (which later got confirmed by the hint).

The torrent specification describes an optional field for md5 checksums of the files it contains (https://wiki.theory.org/BitTorrentSpecification) so I tried to read it, but alas, it was empty.

Then it hit me, the file was named `every_ip_address.txt` so it was probally a text file lisiting the entire IPV4 address range. So I wrote up a simple python script that iterates each address:
```python
for a in range(0,256):
	for b in range(0,256):
		for c in range(0,256):
			for d in range(0,256):
				string = "%s.%s.%s.%s" % (a,b,c,d)
				print string
```

Running it and piping the output to `md5sum` gave us the flag:
```
root@kali:~# python ip.py | md5sum
1a97f624cc74e4944350c04f5ae1fe8d
```

## Other write-ups and resources

* [Matir’s writeup](https://systemoverlord.com/blog/2014/05/19/def-con-22-ctf-quals-hackertool/)
* <https://hackucf.org/blog/hackertool/>
* <http://delogrand.blogspot.de/2014/05/defcon-2014-quals-hackertool.html>
