# Plaid CTF 2014: curlcore

**Category:** Forensics
**Points:** 250
**Description:**

> We managed to grab a [memory dump](curlcore-b9b2bc016a796db9db66be6365d48a6b.tar.bz2) off of The Plague's computer while he was making a secure download. We think he may have been looking for new places to hide the Prime Factorizer. Can you figure out what messages were sent through his computer?

## Write-up

(TODO)

```
23:52:26 <iZsh> tylerni7: you get the sessionID from wireshark, you search for this, and the masterkey is just before that key, then you feed that to wireshark and that's it
00:02:13 <inter> what was the methods to find the aes key in the corefile?
00:02:25 <iZsh> inter: you can open it in wireshark, look at the SessionID, search for it in a hex editor in the dump, just before that, you'll have the size of the sessionid, and then before that, the masterkey
00:02:25 <geobot> and the masterkey is just before
00:02:38 <inter> open corefile?
00:02:48 <inter> oh
00:02:49 <inter> nvm
00:02:50 <inter> OHH
00:02:51 <inter> okay
00:02:52 <iZsh> inter: then you write a file called key.txt which contains the sessionid and the masterkey and you can feed that to wireshark for decryption
00:02:52 <inter> wow
00:03:10 <inter> damn
00:03:28 <inter> it feels like a hammer just slammed my face to the floor
00:03:40 <inter> thanks iZsh :D
00:03:42 <iZsh> that one was fast to solve :)
```

## Other write-ups

* none yet
