# ASIS Cyber Security Contest Finals 2014: TicTac

**Category:** Forensics
**Points:** 200
**Description:**

> Find flag in [this](tictac_4c56077190984fde63900b3ba14d11dd) file

## Write-up

Let’s see what [the provided file](tictac_4c56077190984fde63900b3ba14d11dd) could be:

```bash
$ file tictac_4c56077190984fde63900b3ba14d11dd
tictac_4c56077190984fde63900b3ba14d11dd: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < tictac_4c56077190984fde63900b3ba14d11dd > tictac`
* `unxz < tictac_4c56077190984fde63900b3ba14d11dd > tictac`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x tictac_4c56077190984fde63900b3ba14d11dd
```

Let’s find out what the extracted file is:

```bash
$ file tictac
tictac: data
```

However, `tictac` seems to be a packet capture file.
Running `strings` on this file reveals a number of hex-encoded strings:

```
7069636b206d653a204153
7069636b206d653a204153
7069636b206d653a204953
7069636b206d653a204953
7069636b206d653a205f36
7069636b206d653a206435
7069636b206d653a206435
7069636b206d653a203461
7069636b206d653a203461
7069636b206d653a203637
7069636b206d653a203637
7069636b206d653a203635
7069636b206d653a203635
7069636b206d653a203965
7069636b206d653a203965
7069636b206d653a203435
7069636b206d653a206564
7069636b206d653a206265
7069636b206d653a203633
7069636b206d653a206262
7069636b206d653a206639
7069636b206d653a203039
7069636b206d653a203039
7069636b206d653a206536
7069636b206d653a206231
7069636b206d653a203833
7069636b206d653a203833
7069636b206d653a206120
7069636b206d653a206120
7069636b206d653a20
7069636b206d653a20
```

The first decoded to `pick me: AS`, indicating it probably contains the flag:

```bash
$ head -1 extracted-hex.txt | xxd -r -ps
pick me: AS
```

Some hex-strings are duplicates, so we only take the unique ones and decode
all of them to form the flag:

```bash
$ uniq extracted-hex.txt | xxd -r -ps | sed 's/pick me: //g'
ASIS_6d54a67659e45edbe63bbf909e6b183a
```

## Other write-ups and resources

* <http://www.mrt-prodz.com/blog/view/2014/10/asis-ctf-finals-2014---tictac-200pts-writeup>
* <http://shankaraman.wordpress.com/2014/10/14/asis-ctf-2014-finals-tictac-writeup/>
* <http://tasteless.eu/2014/10/asis-ctf-finals-2014-tictac-forensics-200/>
* <http://bruce30262.logdown.com/posts/237427-asis-ctf-finals-2014-tictac>
