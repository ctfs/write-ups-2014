# CSAW CTF 2014: Fluffy No More

**Category:** Forensics
**Points:** 300
**Description:**

> OH NO WE'VE BEEN HACKED!!!!!! -- said the Eye Heart Fluffy Bunnies Blog owner. Life was grand for the fluff fanatic until one day the site's users started to get attacked! Apparently fluffy bunnies are not just a love of fun furry families but also furtive foreign governments. The notorious "Forgotten Freaks" hacking group was known to be targeting high powered politicians. Were the cute bunnies the next in their long list of conquests!??
>
> Well... The fluff needs your stuff. I've pulled the logs from the server for you along with a backup of its database and configuration. Figure out what is going on!
>
> Written by brad_anton
>
> [CSAW2014-FluffyNoMore-v0.1.tar.bz2](CSAW2014-FluffyNoMore-v0.1.tar.bz2)

## Write-up

(TODO authlog → html5.js → /analytics.js → announcement.pdf)

Opening the PDF file in [PDF Stream Dumper](http://sandsprite.com/blogs/index.php?uid=7&pid=57) reveals some hidden JavaScript code:

![](pdf-stream-dumper.png)

```js
var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];
```

This [is equivalent to](https://mothereff.in/js-escapes#1var%20%5f0xee0b%3D%5B%22%5Cx59%5Cx4F%5Cx55%5Cx20%5Cx44%5Cx49%5Cx44%5Cx20%5Cx49%5Cx54%5Cx21%5Cx20%5Cx43%5Cx4F%5Cx4E%5Cx47%5Cx52%5Cx41%5Cx54%5Cx53%5Cx21%5Cx20%5Cx66%5Cx77%5Cx69%5Cx77%5Cx2C%5Cx20%5Cx6A%5Cx61%5Cx76%5Cx61%5Cx73%5Cx63%5Cx72%5Cx69%5Cx70%5Cx74%5Cx20%5Cx6F%5Cx62%5Cx66%5Cx75%5Cx73%5Cx63%5Cx61%5Cx74%5Cx69%5Cx6F%5Cx6E%5Cx20%5Cx69%5Cx73%5Cx20%5Cx73%5Cx6F%5Cx66%5Cx61%5Cx20%5Cx6B%5Cx69%5Cx6E%5Cx67%5Cx20%5Cx64%5Cx75%5Cx6D%5Cx62%5Cx20%5Cx20%5Cx3A%5Cx29%5Cx20%5Cx6B%5Cx65%5Cx79%5Cx7B%5Cx54%5Cx68%5Cx6F%5Cx73%5Cx65%5Cx20%5Cx46%5Cx6C%5Cx75%5Cx66%5Cx66%5Cx79%5Cx20%5Cx42%5Cx75%5Cx6E%5Cx6E%5Cx69%5Cx65%5Cx73%5Cx20%5Cx4D%5Cx61%5Cx6B%5Cx65%5Cx20%5Cx54%5Cx75%5Cx6D%5Cx6D%5Cx79%5Cx20%5Cx42%5Cx75%5Cx6D%5Cx70%5Cx79%5Cx7D%22%5D%3Bvar%20y%3D%5f0xee0b%5B0%5D%3B):

```js
'var _0xee0b=["YOU DID IT! CONGRATS! fwiw, javascript obfuscation is sofa king dumb  :) key{Those Fluffy Bunnies Make Tummy Bumpy}"];var y=_0xee0b[0];'
```

The flag is `Those Fluffy Bunnies Make Tummy Bumpy`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/09/csaw14-fluffy-no-more-writeup.html>
* <http://sugarstack.io/csaw2014-fluffy-no-more/>
