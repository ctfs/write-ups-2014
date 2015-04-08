# Nuit du Hack CTF Qualifications: Another One

**Category:** Crypto
**Points:** 300
**Description:**

> This is a crypted image, you must extract the data.
>
> [`crypted.bmp`](crypted.bmp)

## Write-up

(TODO: figure out it’s ECB)

This challenge can easily be solved using [ElectronicColoringBook](https://doegox.github.io/ElectronicColoringBook/):

```bash
$ python ElectronicColoringBook.py --flip crypted.bmp
fb5ea1b7895c5e8da75a0ddf0300fe3b     225062 #00 -> #FF #FF #FF
6cdad40fdd970f8acb9fa6647098c452      15709 #7D -> #28 #CC #C0
bbec27cf5e0d0e9de65d06481ee26a9a        928 #42 -> #74 #CC #28
75d1d120fe5d9e605e0e25a2d2a1928f        750 #AA -> #28 #2A #CC
3bca008436fe1eec6254de08293fe33f        588 #A6 -> #28 #39 #CC
820a02cb1f0191f757c95f17eae02e16        227 #58 -> #28 #CC #31
4aa8547d6336592ca6d22fe06a580527        148 #58 -> #28 #CC #31
f77a3852a26c3e3e65504f88293ed1eb        146 #17 -> #CC #7D #28
adf3ba50c7601c792e2303a3171dd902        145 #D3 -> #C5 #28 #CC
a8c0e892b95002c5cadbb48bd0f6d926        110 #82 -> #28 #C4 #CC
879da25d13e929773097dd8586dbf652        104 #8E -> #28 #96 #CC
7e1e4cca7b5c22392267cc23732b558f        103 #FC -> #CC #28 #34
2f3717c1ea26ab6d7273d66c7da36c8f         89 #5E -> #28 #CC #48
4c5eb6b2e6d4e2a0aa31d972d5d406cb         82 #E8 -> #CC #28 #81
734bc30ba09aa6a3a44935011ac2f27e         81 #6C -> #28 #CC #7E
********************************      25732 #FF -> #00 #00 #00
Trying to guess ratio between 1:3 and 3:1 ...
Width: from 692 to 6234
Sampling: 1000
Progress: 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900 5000 5100 5200 5300 5400 5500 5600 5700 5800 5900 6000 6100 6200
Size:  (4800, 900)
```

The flag is `AllMyLifeIThoughtAirWasFreeUntilIBoughtABagOfChips`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/04/nuit-du-hack-quals-another-one-writeup.html>
* <http://wiki.yobi.be/wiki/NDH_Writeups#Another_One>
