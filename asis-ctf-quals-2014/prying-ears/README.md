# ASIS Cyber Security Contest Quals 2014: Prying ears

**Category:** Forensic
**Points:** 175
**Description:**

> [file](forensic_175_1f352928fa34c024c9ab15d102b115ce)

## Write-up

Let’s see what [the provided file](forensic_175_1f352928fa34c024c9ab15d102b115ce) could be:

```bash
$ file forensic_175_1f352928fa34c024c9ab15d102b115ce
forensic_175_1f352928fa34c024c9ab15d102b115ce: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < forensic_175_1f352928fa34c024c9ab15d102b115ce > forensic_175`
* `unxz < forensic_175_1f352928fa34c024c9ab15d102b115ce > forensic_175`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x forensic_175_1f352928fa34c024c9ab15d102b115ce
```

Let’s find out what the extracted file is:

```bash
$ file forensic_175
forensic_175: POSIX tar archive
```

Extract the tar archive:

```bash
$ tar -vxzf forensic_175
x forensic_175_d78a42edc01c9104653776f16813d9e5
```

And inspect the extracted file:

```bash
$ file forensic_175_2ca7d28df77ec506efc36dd09a146b13
forensic_175_d78a42edc01c9104653776f16813d9e5: data
```

The file is a Pcap-ng (Wireshark) file. Running Wireshark’s protocol hierarchy on the file reveals a lot of DNS traffic.
We notice that most of this DNS traffic consists of requests to a domain name with the following format: `[0-9a-f]{14}.asis.io`. However, all of them result in a “not found” response.

Looking closer we see that all of the prefixes to `.asis.io` are hexadecimal digits. The first one is `89504e470d0a1a`, which contains the [magic number](http://en.wikipedia.org/wiki/List_of_file_signatures) for PNG (`89 50 4e 47 0d 0a 1a 0a`). So we extracted all the requests with the `[0-9a-f]{14}.asis.io` format, saved the prefixes to a file and transformed them to a PNG using:

```bash
$ xxd -r -p hex.txt out.png
```

The PNG file contained the flag.

## Other write-ups and resources

* <http://tasteless.eu/2014/05/asis2014-forensics-175-prying-ears/>
* <http://blog.dul.ac/2014/05/ASISCTF14/>
