# SECCON CTF 2014: Get from curious “FTP” server

**Category:** Network
**Points:** 300
**Description:**

> ftp://ftpsv.quals.seccon.jp/

## Write-up

```bash
$ ftp ftpsv.quals.seccon.jp
Connected to ftpsv.quals.seccon.jp.
220 (vsFTPd 2.3.5(SECCON Custom))
Name (ftpsv.quals.seccon.jp:mathias): anonymous
ano331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||6816|).
502 LIST not implemented.
ftp>
```

Let’s try using `nc` instead so we can send raw FTP commands more easily:

```
$ nc ftpsv.quals.seccon.jp 21
220 (vsFTPd 2.3.5(SECCON Custom))
USER anonymous
331 Please specify the password.
PASS anonymous
230 Login successful.
LIST
502 LIST not implemented.
STAT .
213-Status follows:
drwxr-xr-x    2 0        107          4096 Nov 29 04:43 .
drwxr-xr-x    2 0        107          4096 Nov 29 04:43 ..
-rw-r--r--    1 0        0              38 Nov 29 04:43 key_is_in_this_file_afjoirefjort94dv7u.txt
213 End of status
^C
```

The `STAT` command can be used with a parameter [in which case it’s similar to the `LIST` command](http://www.nsftools.com/tips/RawFTP.htm#STAT). Now that we know the file name, let’s request it:

```bash
$ curl 'ftp://ftpsv.quals.seccon.jp/key_is_in_this_file_afjoirefjort94dv7u.txt'
SECCON{S0m3+im3_Pr0t0c0l_t411_4_1i3.}
```

The flag is `SECCON{S0m3+im3_Pr0t0c0l_t411_4_1i3.}`.

## Other write-ups and resources

* <http://tasteless.eu/2014/12/seccon-ctf-2014-online-qualifications-net300-writeup/>
