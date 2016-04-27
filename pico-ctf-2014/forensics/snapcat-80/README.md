# Pico CTF 2014 : Snapchat

**Category:** Forensics
**Points:** 80
**Description:**

>It was found that a Daedalus employee was storing his personal files on a work computer. Unfortunately, he corrupted the filesystem before we could prove it. Can you take a look? Download here.

**Hint:**
>It seems like data recovery can be performed on the disk.img--maybe you'll find something?

## Write-up

We can start by trying `strings` on the file to see what it outputs

```
$ strings disk.img
PICTURES   
driEEEE
ziEE
.          
dniEEEE
niEE
..         
dniEEEE
niEE
BILLY   JPG 
driEEEE
riEE
LAG    JPG 
driEEEE
riEE1
FUZZY   JPG 
driEEEE
riEE8
PEW     JPG 
driEEEE
riEE
PRECIOUSJPG 
driEEEE
riEE
JFIF
<............ more random data........>
```

The image seems to contain some pictures apparently. We can try to recover them with `foremost`

```
$ foremost -v disk.img                                                                                                                                                                                    [master] 
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File

Foremost started
Invocation: foremost -v disk.img 
Output directory: output/
Configuration file: /etc/foremost.conf
Processing: disk.img
|------------------------------------------------------------------
File: disk.img
Length: 5 MB (5242880 bytes)
 
Num  Name (bs=512)         Size  File Offset     Comment 

0:  00000057.jpg          89 KB           29184      
1:  00000237.jpg          13 KB          121344      
2:  00000265.jpg         172 KB          135680      
3:  00000613.jpg          34 KB          313856      
4:  00000685.jpg          56 KB          350720      
*|
Finish: Sat Mar 12 13:48:30 2016

5 FILES EXTRACTED
    
jpg:= 5
------------------------------------------------------------------

Foremost finished
```

We check the images in the output directory and one of them displays the flag 
`i_can_has_cheezburger`

## Other write-ups and resources

* <http://ehsandev.com/pico2014/forensics/snapcat.html>
