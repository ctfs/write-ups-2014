# ASIS Cyber Security Contest Finals 2014: Fact or Real?

**Category:** Recon
**Points:** 25
**Description:**

> `ASIS_md5(motto)`

## Write-up

_factoreal_ is one of the organizers of this CTF. On [his Twitter account](https://twitter.com/factoreal) we find [a tweet with the text “fact or real:” followed by an image that says `NO+$=YES`](https://twitter.com/factoreal/status/486459604973662208).

```bash
$ md5 -s 'NO+$=YES'
MD5 ("NO+$=YES") = d25b9c2f1c29e49e81e8fdfaf4d16fc6
```

The flag is `ASIS_d25b9c2f1c29e49e81e8fdfaf4d16fc6`.

## Other write-ups and resources

* <http://www.mrt-prodz.com/blog/view/2014/10/asis-ctf-finals-2014---fact-or-real-75pts-writeup>
