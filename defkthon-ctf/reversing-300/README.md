# DEFKTHON CTF: Reversing 300

**Description:**

> [Password](300.exe)

## Write-up

_This write-up is made by the [HacknamStyle](http://hacknamstyle.net/) CTF team._

So `file 300.exe` says that it’s an ordinary PE32 windows executable. When opening it in IDA and viewing all the strings referenced by the program, we see a lot of Python API functions that are dynamically loaded. It turns out the executable is also a valid ZIP file, and this zip file contains the `hashlib` python module. This is an open source module, suggesting that the program somehow uses this module to check the password entered by the user.

We want to extract the embedded python code. One string located close to the python API function names is `_MEIPASS2`. This string is an environment variable used by [PyInstaller](http://www.pyinstaller.org/export/develop/project/doc/Manual.html). Lucky for us, PyInstaller has a tool called ArchiveViewer to extract Python code from a created executable. Using `ArchiveViewer.py` we extract the python file `challenge1`:

```py
#AJIN ABRAHAM | OPENSECURITY.IN
from passlib.hash import cisco_pix as pix
import sys,base64
user=""
xx=""
if(len(sys.argv)>1):
     x=sys.argv[1]
     hashus = pix.encrypt("DEFCON14-CTF-IS", user=x)
     z=[89,86,69,121,100,82,69,103,98,47,48,103,80,71,77,121]
     for zz in z:
          xx+= chr(zz+(275*100001-275*1000-27225274))
     hashgen = pix.encrypt("DEFCON14-CTF-IS", user=base64.decodestring(xx))
     if(hashgen==hashus):
          print "Oh Man You got it! But :( ===>    " + str(base64.encodestring(base64.decodestring(xx)))
     else:
          print "Naaaaaaa !! You are screweD"
else:
     print "Password !!"
```

As you can see, it stores the password in obfuscated form. Then it uses the key `DEFCON14-CTF-IS` to encrypt both the stored password, and the password entered by the user. We can easily find the password by including the line `print base64.decodestring(xx)`. This prints `easy!asMa@ss`.

## Other write-ups and resources

* <http://rce4fun.blogspot.com/2014/03/defkthon-ctf-2014-reversing-300-writeup.html>
* [Japanese](http://hority-ctf.blogspot.jp/2014/03/defkthon-ctf-2014-write-up.html)
