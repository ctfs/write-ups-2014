# ASIS Cyber Security Contest Quals 2014: forensic

**Category:** Forensic
**Points:** 150
**Description:**

> [file](forensic_150_d0a3ca9740270f3b30e56c9cfa3050f3)

## Write-up

The file contained a pcap file. 
We fired up a quick packet search with wireshark on the string "flag" in the packet bytes. All results seem to be comments to some html/javascript code about a boolean variable (a flag).   
Except for one result, which seems to be the result of a file download called 'myfile'.   
Extracting this file from the pcap and using the linux file command we see that 'myfile' is actually another pcap file. However loading it in wireshark doesn't seem to work, the file is broken.   
We ran pcapfix on 'myfile' which succesfully repaired it so it could be opened in wireshark.   
Investigating this file reveals a file upload to a hp device, most likely a printer.   
Again, we extract this file which resulted in a postscript file that contained the flag in ascii art.

## Other write-ups

* none yet
