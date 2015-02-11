# 2014 Secuinside CTF Prequal: Mic Check

**Category:** Speed Game
**Points:** 7
**Description:**

> `Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3Ei`

## Write-up

The given string looks like a base64 encoded string. However, decoding it does not reveal anything legible:

```bash
$ base64 --decode <<< 'Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E' | xxd
0000000: 4364 274f 6f68 50d5 b4c2 d5aa c920 dbc3  Cd'OohP...... ..
0000010: 6521 bd12 244d 1adb cb64 1dc7 6834 50e8  e!..$M...d..h4P.
0000020: dbc0 21e8 4d1a e9                        ..!.M..
```

So it might be encrypted with a cipher, lets try the go-to caesar cipher and decrypt all rot combinations, e.g. using [this code](https://github.com/YASME-Tim/crypto-tools/blob/master/rot/rot.py).

```bash
$ for i in {0..52}; do python rot.py $i 'Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E'; done
Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E
Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E
Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E
[...]
Q2QmT29nUNW0vsWpxSDav2UguRIjTRqax2Qcw2f0UOiavCHnTRqov3E
P2PnS29oTMV0wtVqyRCbw2ThvQHkSQrby2Pdx2g0TNjbwBGoSQrpw3D
Q2QnT29oUNW0wtWqySDbw2UhvRIkTRrby2Qdx2g0UOjbwCHoTRrpw3E
```

Note that my code tries several options (Rotate lowercase only, rotate uppercase only, rotate seperate from each other or rotate over lower concatted with upper alphabet).

After decrypting each result, we find that `V2VsY29tZSB0byBvdXIgb2ZmaWNpYWwgd2Vic2l0ZTogbHMtYWwub3J` is the base64 encoded string we are looking for.

It yields the flag `Welcome to our official website: ls-al.`.
## Other write-ups and resources

* <http://atdog.logdown.com/posts/2014/06/02/secuinside-2014-ctf-misc-7>
* <https://ucs.fbi.h-da.de/writeup-secuinside-ctf-quals-2014-speed-games/>
* <http://hacktracking.blogspot.de/2014/06/secuinside-ctf-quals-2k14-speed-game.html>
* <https://www.dropbox.com/sh/ytfak01xhkjkiwp/AABcoW-29SN9M4HZ_U7PNsDma/writeup-SpeedGame.pdf>
