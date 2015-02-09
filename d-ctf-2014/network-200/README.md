# D-CTF 2014: Network 200 – The Manager is back

**Category:** Network
**Points:** 200
**Description:**

> That fucking manager got smarter. He moved to house number 22, but we got this: [fuckmanagers.pcap](manager.pcap)

## Write-up

After looking at [the provided packet capture file](manager.pcap) in Wireshark for a while, we spot a single `POST` request (easily visible using the `http.request.method == "POST"` filter). Right-click on the packet and select _Copy_ → _Bytes_ → _Printable Text Only_ to get its details:

```
E8@@


%RP5gO*M
odLPOST / HTTP/1.1
Host: 10.13.37.22
Connection: keep-alive
Content-Length: 89
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://10.13.37.22
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://10.13.37.22/
Accept-Encoding: gzip,deflate
Accept-Language: en-US,en;q=0.8,ro;q=0.6,ru;q=0.4
Cookie: PHPSESSID=7hnoc09he3vtohslep97fdm8o0

user=manager&nonce=7413734ab666ce02cf27c9862c96a8e7&pass=3ecd6317a873b18e7dde351ac094ee3b
```

There is indeed a login form hosted at `http://10.13.37.22/` (“house number 22”). Let’s try submitting the same username, nonce, and password as found in the packet capture file:

```bash
$ curl --data 'user=manager&nonce=7413734ab666ce02cf27c9862c96a8e7&pass=3ecd6317a873b18e7dde351ac094ee3b' http://10.13.37.22/
Invalid nonce.
```

Ah, that would’ve been too easy.

Looking more closely at the login page, we find out the password is hashed and XORed with a nonce on the client-side before submitting it as `POST` data:

```js
$('.hook-submit').click(function(){
  var h1 = md5($('#pass').val());
  var h2 = $('#nonce').val();
  var xor = myxor(h1, h2);
  $('#hiddenpass').val(xor);
  setTimeout(function() { $('#form').submit(); }, 100);
});
```

This means that the `password` value that was recorded in the packet capture file (i.e. `3ecd6317a873b18e7dde351ac094ee3b`) is the result of `myxor(md5(password), '7413734ab666ce02cf27c9862c96a8e7')` for some value of `password`.

```
'3ecd6317a873b18e7dde351ac094ee3b' == myxor(md5(password), '7413734ab666ce02cf27c9862c96a8e7')
```

However, some quick testing reveals that the `myxor` function is not actually a XOR implementation:

```js
myxor('a', 'a');
// → '4'
myxor('b', 'b');
// → '6'
```

A true XOR function would return `0` in both cases (since `A ⊕ A = 0` for XOR ciphers).

All we need to do is find out what the original value of `password` was. Actually, it would be sufficient to find out what `md5(password)` was – then we could just `myxor()` it with the nonce the page presented, and submit that as `POST` data.

To do either of these things, we have to reverse the `myxor()` function as found in <http://10.13.37.22/js/scripts.js>. Here’s what the original code looks like:

```js
function is_numeric(mixed_var) {
  var whitespace =
    " \n\r\t\f\x0b\xa0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b\u2028\u2029\u3000";
  return (typeof mixed_var === 'number' || (typeof mixed_var === 'string' && whitespace.indexOf(mixed_var.slice(-1)) === -
    1)) && mixed_var !== '' && !isNaN(mixed_var);
}

function ord(string) {
  var str = string + '',
    code = str.charCodeAt(0);
  if (0xD800 <= code && code <= 0xDBFF) {
    var hi = code;
    if (str.length === 1) {
      return code;
    }
    var low = str.charCodeAt(1);
    return ((hi - 0xD800) * 0x400) + (low - 0xDC00) + 0x10000;
  }
  if (0xDC00 <= code && code <= 0xDFFF) {
    return code;
  }
  return code;
}

function chr(codePt) {

  if (codePt > 0xFFFF) {
    codePt -= 0x10000;
    return String.fromCharCode(0xD800 + (codePt >> 10), 0xDC00 + (codePt & 0x3FF));
  }
  return String.fromCharCode(codePt);
}

function hex2n(c) {
  if(is_numeric(c)) return parseInt(c);
  return ord(c) - ord('a') + 10;
}

function n2hex(n) {
  if(n < 10) { return '' + n; }
  return chr(ord('a') + n - 10);
}

function myxor(h1, h2) {
  var xored = '';
  for(i = 0; i<h1.length; i++) {
    var c1 = h1.charAt(i);
    var c2 = h2.charAt(i);
    xored += n2hex((hex2n(c1) + hex2n(c2)) % 16);
  }
  return xored;
}
```

After reversing, that becomes:

```js
function reversemyxor(xored) {
  var h2 = '7413734ab666ce02cf27c9862c96a8e7'; // The nonce that was used by the manager.
  var h1 = '';
  for (var i = 0; i < xored.length; i++) {
    var x1 = xored.charAt(i); // == n2hex((hex2n(c1) + hex2n(c2)) % 16)
    var c2 = h2.charAt(i);
    // Find `c1`, knowing that:
    // x1 == n2hex((hex2n(c1) + hex2n(c2)) % 16)
    // hex2n(x1) == (hex2n(c1) + hex2n(c2)) % 16
    // hex2n(x1) == ((hex2n(c1) % 16) + (hex2n(c2) % 16)
    // hex2n(x1) - (hex2n(c2) % 16) == hex2n(c1) % 16
    // n2hex(hex2n(x1) - (hex2n(c2) % 16)) == c1
    var number = hex2n(x1) - (hex2n(c2) % 16);
    if (number < 0) {
      number += 16;
    }
    var c1 = n2hex(number);
    h1 += c1;
  }
  return h1;
}
```

With this, we can find out what `md5(password)` was for the manager, before it got XORed with the nonce `7413734ab666ce02cf27c9862c96a8e7`:

```js
reversemyxor('3ecd6317a873b18e7dde351ac094ee3b');
// → 'cabaf0ddf21df38cbeb77c94a40e4654'
```

Since `cabaf0ddf21df38cbeb77c94a40e4654` is not a known MD5 hash, we cannot easily find out what the actual password is. But we can use this MD5 hash and XOR it with the nonce we get when we open the login page, and then submit the resulting values as `POST` data. Here’s a JavaScript snippet that does just that — run it in your favorite browser’s DevTools console on the login page:

```js
// XOR the hash we found with the given nonce.
var nonce = $('#nonce').val();
var hash = 'cabaf0ddf21df38cbeb77c94a40e4654';
var xored = myxor(hash, nonce);

// Fill out the form.
$('#user').val('manager');
$('#pass').val(xored);
$('#hiddenpass').val(xored);

// Remove the existing hooks.
$('.hook-submit').unbind();

// Submit the form.
$('#form').submit();
```

After this, we are successfully logged in, and the website displays this message:

> The secret is behind bb00403ebcbfa0748bcbee426acfdb5b :)

A quick Google search reveals that `bb00403ebcbfa0748bcbee426acfdb5b` is the MD5 hash for the string `youtoo`.

The flag is `youtoo`.

### Alternate solution

Similar to how the Network 100 challenge was solved by SSHing into the box, we successfully SSHed into Network 200’s box using `ssh guest@10.13.37.22` and `guest` as the password.

Navigating and listing the directory of `/var/www` gave up a `html` folder, and `ls /var/www/html` reveals some folders and an `index.php` file. Running `cat /var/www/html/index.php` reveals some interesting PHP code at the top of the file. One line reads:

> The secret is behind bb00403ebcbfa0748bcbee426acfdb5b :)

Googling `bb00403ebcbfa0748bcbee426acfdb5b` reveals that it is the MD5 hash of the string `youtoo`, which is the flag.

## Other write-ups and resources

* <http://www.mrt-prodz.com/blog/view/2014/10/defcamp-ctf-quals-2014---network-200--the-manager-is-back-200pts-writeup/>
