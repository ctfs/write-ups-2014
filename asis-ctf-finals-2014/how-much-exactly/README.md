# ASIS Cyber Security Contest Finals 2014: How much exactly?

**Category:** Trivia
**Points:** 25
**Description:**

> 4046925: How much the exact IM per year?
>
> `flag=ASIS_md5(size)`

## Write-up

Googling for ‘4046925’ leads to [NSA DOCID: 4046925 Untangling the Web: A Guide to Internet Research](https://www.nsa.gov/public_info/_files/untangling_the_web.pdf). Searching that document for “instant messaging” (IM), we find:

> Instant messaging generates five billion messages a day (750GB), or 274 Terabytes a year.

```bash
$ md5 -s '274'
MD5 ("274") = d947bf06a885db0d477d707121934ff8
```

The flag is `ASIS_d947bf06a885db0d477d707121934ff8`.

## Other write-ups

* none yet
