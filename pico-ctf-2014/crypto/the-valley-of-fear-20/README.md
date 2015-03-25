# Pico CTF 2014 : The Valley Of Fear

**Category:** Crypto
**Points:** 20
**Description:**

>The hard drive may be corrupted, but you were able to recover a small chunk of text. Scribbled on the back of the hard drive is a set of mysterious numbers. Can you discover the meaning behind these numbers? (1, 9, 4) (4, 2, 8) (4, 8, 3) (7, 1, 5) (8, 10, 1)

**Hint:**
>Might each set of three numbers represent a word in a message?

## Write-up

The hint tells us that each of these three numbers might represent a word in a message.

We are given 9 paragraphs in [book.txt]() with up to 17 lines for each sentence and quickly discover that each triple uses following scheme to encodes/hide a word:

```
(1, 9, 4) === (paragraph, line-in-paragraph, word-in-line) === 4th word in 9th line of first paragraph
```

That means we get following words:

```
(1,  9, 4) === the
(4,  2, 8) === flag
(4,  8, 3) === is
(7,  1, 5) === Ceremonial
(8, 10, 1) === plates
```

The flag is `Ceremonial plates`.

## Other write-ups and resources

* <http://ehsandev.com/pico2014/cryptography/the_valley_of_fear.html>
* <https://ctf-team.vulnhub.com/picoctf-2014-the-valley-of-fear/>
* <https://github.com/PizzaEaters/picoCTF-2014/tree/master/valley>
