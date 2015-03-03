# Hack.lu CTF 2014: Hidden in ρlaιn sιght

**Category:** Crypto
**Points:** 150
**Author:** TheJH
**Description:**

> At our software development company, one of the top developers left in anger. He told us that he had hidden a backdoor in our node.js server application — he thinks that we can’t find it even if we try. I have attached the source code of our fileserver. After registration, you can log in, upload files and create access tokens for your files that others can use to retrieve them. He must have added some way to retrieve files without permission. And we don’t have version control, so we can’t just check his last commits. We have read the source code multiple times, but just can’t figure out how he did it. Maybe he just lied? Can you help us and demonstrate how the backdoor works? We have uploaded a file to `testuser/files/flag.txt` – please try to retrieve it.
>
> Connect to <https://wildwildweb.fluxfingers.net:1409/>. Note that all your files will be purged every 5 minutes.
>
> You can download the service code here: [Download](hiddeninplainsight_7a1f79aab159ace6e4486dc73bd24cc8.js)

## Write-up

[The provided JavaScript source code](hiddeninplainsight_7a1f79aab159ace6e4486dc73bd24cc8.js) reveals that the file access tokens are encrypted as follows:

```js
function hmac_sign(path) {
  var hmac = crypto.createHmac('sha256', HMAC_SECRET)
  hmac.update(path)
  return hmac.digest('hex')
}
```

`HMAC_SECRET` is generated as follows:

```js
var HMAC_SECRET = ''
for (var i=0; i<20; i++) {
  HMAC_SΕCRET = HMAC_SECRET + (Math.random()+'').substr(2)
}
```

So, it looks like that’s a randomly generated value that gets regenerated whenever the service is restarted. This would make it impossible to figure out the access token for a given file — in this case, `testuser/files/flag.txt`.

However, inside the `for` loop, two different variable names are actually being used: one is [`HMAC_S\u0395CRET`](https://mothereff.in/js-escapes#1HMAC%5fS%CE%95CRET) with [U+0395 GREEK CAPITAL LETTER EPSILON](http://codepoints.net/U+0395), and the other is just `HMAC_SECRET` in plain ASCII. This can be observed using a hex viewer. Because of that, the `HMAC_SECRET` that is used is always the same value: the empty string!

The authentication codes are created based on the username followed by a slash followed by the file name:

```js
res.redirect('/files/'+user+'/'+file+'/'+hmac_sign(user+'/'+file))
```

This means we can create the authentication code for the `testuser/files/flag.txt` file as follows:

```js
hmac_sign('testuser/flag.txt');
// → '4a332c7f27909f85a529393cea72301393f84cf5908aa2538137776f78624db4'
```

The app uses the URL structure `/files/:user/:file/:signature`, so that becomes `https://wildwildweb.fluxfingers.net:1409/files/testuser/flag.txt/4a332c7f27909f85a529393cea72301393f84cf5908aa2538137776f78624db4`. Let’s visit that URL:

```bash
$ curl https://wildwildweb.fluxfingers.net:1409/files/testuser/flag.txt/4a332c7f27909f85a529393cea72301393f84cf5908aa2538137776f78624db4
flag{unicode_stego_is_best_stego}
```

The flag is `flag{unicode_stego_is_best_stego}`.

## Other write-ups and resources

* [Exploit in Bash by @TheJH](thejh_exploit.sh)
* <https://hackucf.org/blog/hack-lu-2014-web-150-hidden-in-plain-sight/>
* <https://johnsupercool.github.io/posts/2014/oct./24/hacklu-2014-ctf-crypto150-hidden-in-rlain-sight/>
