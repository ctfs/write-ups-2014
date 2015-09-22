# Plaid CTF 2014: WhatsCat

**Category:** Web
**Points:** 300
**Description:**

> The Plague is using his tremendous talent for web applications to build social websites that will get bought out for billions of dollars. If you can stop his climb to power now by showing how insecure [this site really is](http://54.196.116.77/), (on IPv6 at 2001:470:8:f7d::1) maybe we will be able to stop his future reign of terror. [Here](whatscat-59b6f6c9b192457fa3e7d2253c8b24c9.tar.bz2)'s some of his source.

## Write-up

The source code in the tarball has a SQL injection vulnerability in the `login` file.

```php
$pwnew = "cat".bin2hex(openssl_random_pseudo_bytes(8));
if ($res) {
  echo sprintf("<p>Don't worry %s, we're emailing you a new password at %s</p>",
    $res->username,$res->email);
  echo sprintf("<p>If you are not %s, we'll tell them something fishy is going on!</p>",
    $res->username);
$message = <<<CAT
Hello. Either you or someone pretending to be you attempted to reset your password.
Anyway, we set your new password to $pwnew

If it wasn't you who changed your password, we have logged their IP information as follows:
CAT;
  $details = gethostbyaddr($_SERVER['REMOTE_ADDR']).
    print_r(dns_get_record(gethostbyaddr($_SERVER['REMOTE_ADDR'])),true);
  mail($res->email,"whatscat password reset",$message.$details,"From: whatscat@whatscat.cat\r\n");
  mysql_query(sprintf("update users set password='%s', resetinfo='%s' where username='%s'",
          $pwnew,$details,$res->username));
}
else {
  echo "Hmm we don't seem to have anyone signed up by that name";
}
```

There’s no way the generated value of `$pwnew` could ever contain `'`, so we can’t use that as part of the exploit. The same goes for the user’s IP address (`$_SERVER['REMOTE_ADDR']`).

However, `dns_get_record(gethostbyaddr($_SERVER['REMOTE_ADDR']))` is also used in the query without proper escaping. So we could get a server, change its [DNS PTR record](http://en.wikipedia.org/wiki/Reverse_DNS_lookup) so the server IP points to a domain name under our control, and configure a TXT record that contains a SQL injection payload on that domain. [Alexey Kaminsky has a write-up detailing this solution.](http://akaminsky.net/plaidctf-quals-2014-web-300-whatscat/) Alternatively, you could set up your own DNS server for this challenge, and have it automatically inject TXT records with the payload, [like @phiber did](https://gist.github.com/anonymous/ea292c8dc60a2d8fba50).

Another option is to hide the SQL injection payload in the username. The downside of this approach is that since the username is reflected in the `WHERE` clause of the query, only blind SQL injection is possible. Still, it’s possible to slowly leak data:

1. Register with username `foo`.
2. Register with username `foo' and 21=(select length(flag) from flag)#`.
3. Request a password reset for the second user.
4. Log in with the first username and its original password. If the password is rejected, then the condition in the payload (in this case `21 == length(flag)` is true, else it’s false.

After discovering the table and column name where the flag is hidden (they’re both `flag`), we can repeat this process to figure out what the flag is, one character at a time. For example, the username `foo' and (select ascii(substr(flag,1,1) from flag) between 97 and 122#` can be used to find out if the first character of the flag is a lowercase letter in the `[a-z]` range or not.

@ngocdh wrote [a neat solution in Python](https://gist.github.com/anonymous/f4e884a234ba5d3c9d37) that uses a clever implementation of this technique: it uses binary search to decrease the time needed to find the correct character.

The flag is `20billion_d0llar_1d3a`.

## Other write-ups and resources

* [Write-up by Alexey Kaminsky](http://akaminsky.net/plaidctf-quals-2014-web-300-whatscat/)
* [Write-up by Tasteless](http://tasteless.eu/2014/04/plaidctf-2014-whatscat-writeup/)
* [Write-up by Ron Bowes](https://blog.skullsecurity.org/2014/plaidctf-writeup-for-web-300-whatscat-sql-injection-via-dns)
* [Python solution that figures out the flag character by character, by @ngocdh](https://gist.github.com/anonymous/f4e884a234ba5d3c9d37)
* [Custom DNS server to perform SQL injection through rDNS records, by @phiber](https://gist.github.com/anonymous/ea292c8dc60a2d8fba50)
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/whatscat)
