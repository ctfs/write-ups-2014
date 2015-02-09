# Hack.lu CTF 2014: Wanted: Translator

**Category:** Misc
**Points:** 35
**Author:** qll, javex
**Description:**

> Legend says there is a bank vault in Jamestown which cannot be broken into. The only way inside is through an authentication process. Even Jesse James and his companions failed to break the security of this particular bank. Can you do it?
>
> (That means you can send us 7 solutions to this challenge and will receive 5 points for each.)
>
> * SMTP
> * GOPHER
> * POP3
> * FINGER
> * TFTP
> * IRC
> * NNTP

## Write-up

In general, these challenges could be solved by connecting to wildwildweb.fluxfingers.net or 149.13.33.84 using the correct ports, and then messing around with the protocol commands a little bit.

### SMTP

```bash
$ telnet wildwildweb.fluxfingers.net 25
T: Trying 149.13.33.84...
T: Connected to wildwildweb.fluxfingers.net.
T: Escape character is '^]'.
S: 220 protocols FluxSMTPd (send a mail to our team's mail address)
C: HELO fluxmail
S: 250 protocols
C: MAIL FROM: <my-name@example.com>
S: 250 OK
C: RCPT TO:<fluxfingers@ruhr-uni-bochum.de>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: from: my-name@example.com
C: subject: Can haz flag?
C:
C: Can haz flag?
C: .
S: 200 flag{deliver_that_yourself_:-P}
```

### GOPHER

```bash
$ telnet wildwildweb.fluxfingers.net 70
Trying 149.13.33.84...
Connected to wildwildweb.fluxfingers.net.
Escape character is '^]'.

0flag.txt 0 wildwildweb.fluxfingers.net 70
.
Connection closed by foreign host.

$ telnet wildwildweb.fluxfingers.net 70
Trying 149.13.33.84...
Connected to wildwildweb.fluxfingers.net.
Escape character is '^]'.
0
flag{ever_heard_of_g0pher?}
Connection closed by foreign host.
```

### POP3

```bash
$ telnet 149.13.33.84 110
Trying 149.13.33.84...
Connected to 149.13.33.84.
Escape character is '^]'.
+OK POP3 server ready (USER: flux, PASS: flux)
USER flux
+OK
PASS flux
+OK howdy
LIST
+OK 3 messages (57 octets)
0d 9
1d 39
2d 9
.
RETR 1
+OK 39 octets

Message 2 flag{once_pop3d_never_stop3d}
.
```

### FINGER

```bash
$ telnet 149.13.33.84 79
Trying 149.13.33.84...
Connected to 149.13.33.84.
Escape character is '^]'.
r00t
Login name: r00t  In real life: r00t McR00ty
Office: Luxembourg  Home phone: foo-1337
Directory: /r00t  Shell: /bin/1337shell
Plan: flag{f1nger_me_baby...scnr}
Connection closed by foreign host.
```

### TFTP

```bash
$ tftp 149.13.33.84
tftp> get FLAG
Received 1230 bytes in 0.1 seconds
tftp> ^D

$ cat FLAG
EXT. A JAIL IN MEXICO - DAY

It's an early Friday morning and a patrol car drives up an
unpaved road and parks next to a gutted police car on cinder
blocks. The camera pans with the OFFICER as he exits his car
and walks up to a ramp leading to the babay blue JAIL HOUSE.
He is carrying a greasy bag of fast food.

INT. JAIL LOBBY - DAY

The Officer enters the lobby, tosses the bag of food to his
PARTNER who is sitting at a desk. He grabs a tin cup and
walks over to barred entrance to Block A. Twenty or so
CRIMINALS, from drunks to drug dealers are sleeping
peacefully in their cell on Block A. The Officer rattles the
tin cup between the entrance bar.

INT. JAIL CELLS - DAY

The inmates stir, rubbing their dirty faces and trying to sit
up. The camera dollies slowly down the narrow hallway of the
block which has three cells: Two small ones side by side, and
one bigger cell that faces the block entrance. The sound of
scribbling and business dealing can be heard from inside the
cell. It is AZUL jottin ginto a business ledger while
chatting on his cellular phone. His cell is equipped with a
small desk and a refridgerator. He hangs up the phone and
continues writing.

flag{tftp_as_a_service}
```

### IRC

```bash
$ telnet 149.13.33.84 6667
Trying 149.13.33.84...
Connected to 149.13.33.84.
Escape character is '^]'.
nick x
user a a a a
:wildwildweb.fluxfingers.net 001 x :Hi, welcome to IRC
:wildwildweb.fluxfingers.net 002 x :Your host is wildwildweb.fluxfingers.net
:wildwildweb.fluxfingers.net 251 x :3 clients connected right now
:wildwildweb.fluxfingers.net 422 x :MOTD not set
list
:wildwildweb.fluxfingers.net 322 x #flagchannel 1 :Obtain the flag here
:wildwildweb.fluxfingers.net 323 x :End of LIST
JOIN #flagchannel
:x!a@127.0.0.1 JOIN #flagchannel
:wildwildweb.fluxfingers.net 331 x #flagchannel :Obtain the flag here
:wildwildweb.fluxfingers.net 353 x = #flagchannel :x flagbot
:wildwildweb.fluxfingers.net 366 x #flagchannel :End of NAMES list
:flagbot!flagbot@127.0.0.1 PRIVMSG x :The flag is flag{internetrelaaaaaychat}
```

### NNTP

```bash
$ telnet 149.13.33.84 119
Trying 149.13.33.84...
Connected to 149.13.33.84.
Escape character is '^]'.
200 flux news server ready
LIST
215 list of newsgroups follows
apache.chitchat 0 1 n
justhopi.things 0 1 n
.
GROUP apache.chitchat
211 2 0 1 apache.chitchat group selected
ARTICLE 1
220 1 <1292@apache.FLUX> article retrieved
Message-ID: <1292@apache.FLUX>

Ta na á née see. flag{Not_aNother_sTupid_Protocol}
```

## Other write-ups and resources

* <http://akaminsky.net/hack-lu-ctf-2014-misc-35-wanted-translator/>
