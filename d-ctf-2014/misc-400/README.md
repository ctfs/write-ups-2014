# D-CTF 2014: Misc 400 – Conquest of Gaul

**Category:** Misc
**Points:** 400
**Description:**

> Enter Caesar vault sit at his desk and look for the hidden cabinet box! 10.66.66.3. Don't forget to switch the VPN server.

## Write-up

This server kept going down (the exploit is a once-off), so we were eventually provided with a image.
Since everyone had the image, there would be two ways of solving this.

Way 1) Connect to the FTP server as intended

It turns out you can log in as anonymous/anonymous, and also that the FTP server is Cesar FTP server 0.99g.

That version has a buffer overflow vulnerability in the MKD command (http://secunia.com/advisories/20574/), and there is even a metasploit module! http://www.exploit-db.com/exploits/16713/

Exploiting that vulnerability gets you access.

There is a hidden file on the desktop named 'ThisIsit.txt', and inside that the string "<insert the string here>... Caesar Salad!"

We tried using the entire string as well as 'Caesar Salad!' as a key, but eventually we used just 'Caesar Salad' and that worked as a flag.

Fun challenge, too bad it was down.

Way 2)
We have the machine VM! Just boot it into single user mode, reset the admin password, look on the machine.
We found the file called 'ThisIsIt.txt' and it was done.
This would not be the way to solve the challenge because it is it now how the challenge was intended to be solved.



## Other write-ups and resources

* none yet
