# ASIS Cyber Security Contest Finals 2014: Echo

**Category:** PPC
**Points:** 200
**Description:**

> Connect there:
>
> ```bash
> nc asis-ctf.ir 12433
> ```

## Write-up

Let’s connect to the service:

```bash
$ nc asis-ctf.ir 12433
Go Ahead and find flag :D
```

The service seems to just echo whatever we send it:

```bash
$ nc asis-ctf.ir 12433
Go Ahead and find flag :D
a # ← our input
a # ← response
b
b
```

When the word `flag` is used, the service sends an additional response:

```bash
$ nc asis-ctf.ir 12433
Go Ahead and find flag :D
flag
flag
Kidding Me!
```

When exactly two characters are sent, you get yet another response:

```bash
$ nc asis-ctf.ir 12433
Go Ahead and find flag :D
aa
aa
Be smart!
```

After a lot of trial and error, we discover that the server responds ‘Perfect!’ the first time you send `hi` in the session:

```bash
$ nc asis-ctf.ir 12433
Go Ahead and find flag :D
hi
hi
Perfect!
hi
hi
Be smart!
```

We wrote a script that sends every possible combination of two printable ASCII characters to the service, and let it run for a while. Apparently this is the order of messages the service expected (i.e. you get the ‘Perfect!’ response for each of these if you enter them in this order):

```
"hi"
" a"
"ll"
", "
"wa"
"rm"
"up"
" r"
"ou"
"nd"
"! "
"th"
"e "
"fl"
"ag"
" i"
"s "
"AS"
"IS"
"_7"
"17"
"ef"
"53"
"de"
"3a"
"7c"
"90"
"80"
"ef"
"d2"
"bc"
"2b"
"a5"
"d0"
"d0"
```

This gave us the flag except for the last digit. But since we know it’s a hex digit, we can try all options and see which one gets accepted. The flag turned out to be `ASIS_717ef53de3a7c9080efd2bc2ba5d0d05`.

## Other write-ups and resources

* none yet
