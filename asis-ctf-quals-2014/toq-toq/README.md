# ASIS Cyber Security Contest Quals 2014: Toq-Toq

**Category:** Forensic
**Points:** 100
**Description:**

> [file](forensic_100_c920dfa687ed1bf550783407025586f1)

## Write-up

[The provided file](forensic_100_c920dfa687ed1bf550783407025586f1) contains a pcap file. After a quick packet search with Wireshark for the string `flag` in the packet bytes we found some directory listings of a web server, each serving a part of the flag. Here’s all of them:

```html
<li><a href="first_part_of_flag">first_part_of_flag</a>
<li><a href="second_part_of_flag">second_part_of_flag</a>
<li><a href="third_part_of_flag">third_part_of_flag</a>
<li><a href="fourth_part_of_flag">fourth_part_of_flag</a>
<li><a href="last_part_of_flag">last_part_of_flag</a>
```

Sadly, navigating to these pages with a web browser results in a timeout.

Then we thought the “toq toq” challenge name might be a wordplay on “knock knock”, so [port knocking](http://en.wikipedia.org/wiki/Port_knocking) might be needed to open the ports to the webservers.

Using the Wireshark filter `ip.dst==87.107.123.4` a pattern emerges. Right before the webserver is contacted for each request, multiple SYN packets are sent to different ports. Feeding these port sequences to a port knocking script indeed opens the ports which allows us to capture the flag.

Here’s the script we used:

```python
#!/usr/bin/python
# modified version of Eindbazen’s port knocking script

from scapy.all import *
import urllib2

host = "87.107.123.4"

def doPortKnocking(ports, weburl):
  conf.verb = 0
  for dport in range(0, len(ports)):
    #print "[*] Knocking on "+host+": " , ports[dport]
    ip = IP(dst=host)
    port = 39367
    SYN = ip/TCP(sport=port, dport=ports[dport], flags="S", window=2048, options=[('MSS',1460)], seq=0)
    send(SYN)
  response = urllib2.urlopen(weburl)
  html = response.read()
  print html
  response.close() # best practice to close the file

ports = [9264, 11780, 2059, 8334]
print "First part:"
doPortKnocking(ports, 'http://87.107.123.4:24931/first_part_of_flag')

ports = [42304, 53768, 3297, 8334]
print "Second part:"
doPortKnocking(ports, 'http://87.107.123.4:19760/second_part_of_flag')

ports = [23106, 4250, 62532, 11655, 33844]
print "Third part:"
doPortKnocking(ports, 'http://87.107.123.4:3695/third_part_of_flag')

ports = [49377, 48116, 54900, 8149]
print "Fourth part:"
doPortKnocking(ports, 'http://87.107.123.4:31054/fourth_part_of_flag')

ports = [16340, 59991, 37429, 60012, 15397, 21864, 12923, 8799]
print "Last part:"
doPortKnocking(ports, 'http://87.107.123.4:8799/last_part_of_flag')
```

Alternatively, [the `knock` command-line utility](http://www.zeroflux.org/projects/knock) can be used to perform the port knocking.

## Other write-ups and resources

* <http://blog.dul.ac/2014/05/ASISCTF14/>
* [Indonesian](http://blog.rentjong.net/2014/05/toq-toq-forensic100.html)
