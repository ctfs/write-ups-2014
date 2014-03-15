# DEFKTHON CTF: Reversing 400

**Description:**

> [BIN](400.bin)

## Write-up

*This write-up is made by the [hacknamstyle](http://www.hacknamstyle.net) CTF team.*

Running `file 400.bin` gives no useful information: it only detects data. Similarly, `strings 400.bin` also provides no useful information. Executing `binwalk 400.bin` to extract possible hidden files reveals a Squashfs filesystem with a DD-WRT signature. So we're dealing with a DD-WRT firmware image.

Using the firmware-mod-kit and executing `extract-firmware.sh 400.bin` successfully extracts the filesystem. Now the question is how and where the flag is hidden:

1. Is a special password configured somewhere? `grep -ri pass .`, nope.
2. Is a flag in plaintext hidden somewhere? `grep -ri flag .`, YES!

In the file `/var/www/` we encountered the line `</html>'flag is caputdraconis`. Hence the flag to solve this level is caputdraconis.

## Other write-ups

* none yet
