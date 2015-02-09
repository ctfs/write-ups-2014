# Pwnium CTF 2014: break_me

**Category:** Crypto
**Points:** 100
**Description:**
> QlpoOTFBWSZTWTxSmOAAAAsJAF/gOwAgADEAAAiZMNT0JbKzhCQcyQtA2gNbvXgSvxdyRThQkDxSmOA=

## Write-up

We are give with the string that clearly indicates base64 encoding ('=' at the end).
After processing the string with the `base64` command and `file`

    echo 'QlpoOTFBWSZTWTxSmOAAAAsJAF/gOwAgADEAAAiZMNT0JbKzhCQcyQtA2gNbvXgSvxdyRThQkDxSmOA=' | base64 -D > output
    file output
    
we get:
> output: bzip2 compressed data, block size = 900k

After we `unbzip2` it we get the output:
> 9afa828748387b6ac0a393c00e542079

which is the flag.

## Other write-ups and resources

* <https://ctftime.org/writeup/1154>
* <http://krebsco.de/writeups/crack-me.html>
* <https://crazybulletctfwriteups.wordpress.com/2014/07/07/pwnium-ctf-2014-break-me/>
