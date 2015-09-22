# ASIS Cyber Security Contest Quals 2014: Hidden flag

**Category:** Web
**Points:** 75
**Description:** (none)

## Write-up

The detail page for this challenge (available only after login) sends the following HTTP headers:

```
Connection: keep-alive
Content-Encoding: gzip
Content-Language: en-us
Content-Type: text/html; charset=utf-8
Date: Sat, 10 May 2014 13:33:37 GMT
Server: nginx
Transfer-Encoding: chunked
Vary: Cookie, Accept-Language
X-Content-Type-Options: nosniff
x-flag: ASIS_b6b?244608c2?c2e869cb56?67b64?b1
X-Frame-Options: SAMEORIGIN
X-Hacker: Don't Be A Jerk
X-Powered-By: ASIS
X-XSS-Protection: 1; mode = block
```

The `x-flag: ASIS_b6b?244608c2?c2e869cb56?67b64?b1` header value looks like a flag, except four hexadecimal digits have been replaced with question marks. We’ll have to find the right combination of digits, but there are 65,536 possibilities (16 possibilities for each of the 4 digits, i.e. 16 to the power of 4). We definitely cannot submit all of these manually…

Luckily, the challenge detail page contains some JavaScript that validates the flag before submitting it to the server:

```js
$('flag_submission').submit(function(e){
  e.preventDefault();
  var shaObj = new jsSHA(document.forms["flag_submission"]["id_flag"].value, "TEXT");
  var hash = shaObj.getHash("SHA-256", "HEX");
  var shaObj2 = new jsSHA(hash, "TEXT");
  var hash2 = shaObj2.getHash("SHA-256", "HEX");
  if (document.forms["flag_submission"]["check"].value !== hash2) {
    if ($("#id_flag").next().length == 0){
      $('<div class="alert alert-danger" id="answer" />').insertAfter('#id_flag');
    }
    // …
  }
  // …
});
```

It looks like the entered flag gets hashed using SHA-256 twice, and is then compared to the `value` of the `<input>` element with `name="check"`. Let’s see what that value is:

```html
<input id="id_check" name="check" type="hidden" value="2b127c77074e44b6e74074b1eb8d32dfe27fe78e6a05e302baed68e2cc643ca1" />
```

Now that we know `2b127c77074e44b6e74074b1eb8d32dfe27fe78e6a05e302baed68e2cc643ca1` is equal to `sha256(sha256(flag))`, and that flag is some variation of `ASIS_b6b?244608c2?c2e869cb56?67b64?b1`, we can write a script to brute-force the result. Here’s a quick and dirty solution:

```python
#!/usr/bin/env python
# coding=utf-8

import hashlib
import sys

hex_digits = 'abcdef0123456789'
for a in hex_digits:
  for b in hex_digits:
    for c in hex_digits:
      for d in hex_digits:
        flag = 'ASIS_b6b%s244608c2%sc2e869cb56%s67b64%sb1' % (a, b, c, d)
        flagHash = hashlib.sha256(flag).hexdigest()
        checkHash = hashlib.sha256(flagHash).hexdigest()
        if checkHash == '2b127c77074e44b6e74074b1eb8d32dfe27fe78e6a05e302baed68e2cc643ca1':
          print 'Flag found: %s' % flag
          sys.exit()
```

Let’s run it:

```bash
$ python hidden-flag.py
Flag found: ASIS_b6be244608c27c2e869cb56167b649b1
```

The flag is `ASIS_b6be244608c27c2e869cb56167b649b1`.

## Other write-ups and resources

* <http://nickthefrost.com/2014/05/10/asis-ctf-quals-2014-hidden-flag/>
* <http://www.incertia.net/blog/asis-2014-quals-hidden-flag/>
* <http://blogs.univ-poitiers.fr/e-laize/2014/05/11/asis-2014-hiddenflag/>
* <http://tasteless.eu/2014/05/asis-ctf-quals-2014-hidden-flag-writeup/>
* <http://quangntenemy.blogspot.de/2014/05/asis-ctf-quals-2014.html>
* [Persian](http://xploit.ir/asis-2014-quals-%D9%BE%D8%B1%DA%86%D9%85-%D9%85%D8%AE%D9%81%DB%8C/)
* <http://singularityctf.blogspot.de/2014/05/first-of-all-lets-check-headersdata.html>
