# Pico CTF 2014 : Web Instresption

**Category:** Crypto
**Points:** 140
**Description:**

>We were able to get some code running in a Daedalus browser. Unfortunately we can't quite get it to send us a cookie for its internal login page ourselves... But we can make it make requests that we can see, and it seems to be encrypting using ECB mode. See here for more details about what we can get. It's running at [vuln2014.picoctf.com:65414](http://vuln2014.picoctf.com:65414). Can you get us the cookie?

**Hint:**
>In ECB mode, the same plaintext block appearing in two different places leads to the same ciphertext block appearing in both places. Can you figure out how to use this, and the encryption oracle that you have, to decrypt the cookies one byte at a time?

## Write-up

(TODO)

## Other write-ups and resources

* <http://ehsandev.com/pico2014/cryptography/web_interception.html>
* <https://ctf-team.vulnhub.com/picoctf-2014-web-interception/>
* <http://barrebas.github.io/blog/2014/11/06/picoctf-write-ups/>
