# Sharif University Quals CTF 2014: Decrypt the Message!

**Category:** Cryptography
**Points:** 100
**Solves** 36
**Description:**

> Decrypt the message!
>
> [Download](encrypted.txt)

## Write-up

We are given a poem and a ciphertxt:

	The life that I have
	Is all that I have
	And the life that I have
	Is yours.
	
	The love that I have
	Of the life that I have
	Is yours and yours and yours.
	
	A sleep I shall have
	A rest I shall have
	Yet death will be but a pause.
	
	For the peace of my years
	In the long green grass
	Will be yours and yours and yours.
	
	decrypted message: emzcf sebt yuwi ytrr ortl rbon aluo konf ihye cyog rowh prhj feom ihos perp twnb tpak heoc yaui usoa irtd tnlu ntke onds goym hmpq

When searching for `poem cipher`, we find the 'poem code' cipher, explained [here](http://wmbriggs.com/post/1001/) and [here](http://en.wikipedia.org/wiki/Poem_code).

After understanding how this cipher works, we can e.g. use [this code](https://github.com/YASME-Tim/crypto-tools/tree/master/poemcode) to encrypt and decrypt the message.

Note that I had to remove all special characters as well as decrypt the ciphertxt with all possible key/word combinations.

The flag is `ifyouthinkcryptographyistheanswertoyourproblemthenyoudonotknowwhatyourproblemisabcdefghijklmnopqrstu`.

## Other write-ups and resources

* <http://ctf.sharif.edu/2014/quals/su-ctf/write-ups/18/>
