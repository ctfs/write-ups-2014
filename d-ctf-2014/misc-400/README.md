# D-CTF 2014: Misc 400 – Conquest of Gaul

**Category:** Misc
**Points:** 400
**Description:**

> Enter Caesar vault sit at his desk and look for the hidden cabinet box! 10.66.66.3. Don't forget to switch the VPN server.

## Write-up

This server kept going down (the exploit is a once-off), so we were eventually provided with a VirtualBox image. Since everyone had the image, there would be two ways of solving this.

### Intended solution: connect to the FTP server

It turns out you can log in with username `anonymous` and password `anonymous`, and also that the FTP server software is Cesar FTP server 0.99g. That version has [a buffer overflow vulnerability in the `MKD` command](http://secunia.com/advisories/20574/), and there is even [a Metasploit module](http://www.exploit-db.com/exploits/16713/) for it! Exploiting that vulnerability gets you access.

There is a hidden file on the desktop named `ThisIsit.txt`, and inside that the string `you deserve a very nice Caesar Salad!`.

We tried using the entire string as well as `Caesar Salad!` as a key, but eventually we used just `Caesar Salad` and that worked as a flag.

Fun challenge, too bad it was down.

### Alternate solution

We have the machine VM! Just boot it into single user mode, reset the password for the `FTP` Windows user account, and look on the machine. We found the file called `ThisIsIt.txt` and it was done. This was not the intended way to solve the challenge.

### Alternate alternate solution

Even easier, after they handed out the VM image: Simply mount the .vdi and have a look at the file directly.

## Other write-ups and resources

* none yet
