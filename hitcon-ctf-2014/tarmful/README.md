# HITCON CTF 2014: Tarmful

**Category:** Trivia
**Points:** 128
**Description:**
The challenge is a series of archive files inside each other. Each internal zip will be of different format. Initially I tried to open them based on decreasing numbers as well as recognising filetype by names. The final approach I used involved using file magic to detect the filetype and tarfile and zipfile modules to extract the file. Also one of the files had a UTF8 character that caused the extraction to fail. So I just renamed the file and proceeded.

Flag is: HITCON{SO0O0OO_MaNy_7Ar_Le\/eLs}
> Just decompress them all.
> [https://raw.githubusercontent.com/hitcon2014ctf/ctf/master/tarmful-3f13b82f7794de783adfd6fa9928ad2c.zip](tarmful-3f13b82f7794de783adfd6fa9928ad2c.zip)
> [https://dl.dropbox.com/s/oh8cb6i63x7zggh/tarmful-3f13b82f7794de783adfd6fa9928ad2c.zip]()

## Write-up

(TODO)

## Other write-ups

* none yet
