# CONFidence DS CTF Teaser: Stegano50

**Category:** Stegano
**Points:** 50
**Description:**

> Find the hidden message in this [file](stegano50.pdf)

## Write-up

We’re provided with [a PDF file](stegano50.pdf) that mostly contains some _lorem ipsum_ filler text. The document has a watermark saying “No Flag Here!” and also contains this teaser:

> In facilisis et tortor commodo aliquam[ Your flag is not here ]olestie bibendum, leo nisi porttitor massa, id accumsan sapien libero id tellus.

Let’s take a look at the PDF’s meta data.

```bash
$ pdfinfo stegano50.pdf
Title:          polar bear during a snow storm
Subject:        <| tr AB .- |>
Keywords:       Could this be the flag? : Tm9wZSAsIG5vdCBoZXJlIDspCg==
Author:         KeiDii
Creator:        LaTeX /o/
Producer:       find mr.morse text
CreationDate:   Thu Mar 13 22:33:50 2014
ModDate:        Thu Mar 13 22:33:50 2014
Tagged:         no
Form:           none
Pages:          1
Encrypted:      no
Page size:      595.276 x 841.89 pts (A4)
File size:      38742 bytes
Optimized:      no
PDF version:    1.5
```

The ‘keywords’ section seems interesting. Let’s base64-decode `Tm9wZSAsIG5vdCBoZXJlIDspCg==`:

```
$ base64 --decode <<< 'Tm9wZSAsIG5vdCBoZXJlIDspCg=='
Nope , not here ;)
```

That would’ve been too easy! Moving on, the ‘title’ and ‘producer’ fields seem to hint that Morse code is somehow involved. The ‘subject’ field looks like an example of using [the `tr` command](http://unixhelp.ed.ac.uk/CGI/man-cgi?tr): `tr AB .-` means “replace all instances of `A` with `.` and all instances of `B` with `-`”.

Let’s try some other tricks first, though. Using `pdftotext` we can see if the flag is somehow hidden as text in the PDF:

```bash
$ pdftotext stegano50.pdf
```

This produces a file called `stegano50.txt`, which contains another teaser:

```
N

e!

er

oF
la
gH

e!
N

Close - but still not here !

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

L
```

It seems we’re on the right track.

After trying some different PDF to text converters, it turns out opening the PDF in [SumatraPDF](http://blog.kowalczyk.info/software/sumatrapdf/free-pdf-reader.html) on Windows and then saving it as a text file has different results than `pdftotext`. In that case, the output contains some more hidden text (note the `BABA […] AAABB` part):

```
NoFlagHere! NoFlagHere! NoFlagHere!
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Close - but still not here !
BABA BBB BA BBA ABA AB B AAB ABAA AB B AA BBB BA AAA BBAABB AABA ABAA AB BBA BBBAAA ABBBB BA AAAB ABBBB AAAAA ABBBB BAAA ABAA AAABB BB AAABB AAAAA AAAAA AAAAB BBA AAABB
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras faucibus odio ut metus vulputate, id laoreet magna
volutpat. Integer nec enim vel arcu porttitor egestas […]
```

The same text can be viewed by opening the PDF in [PDF.js](http://mozilla.github.io/pdf.js/web/viewer.html), and then inspecting the generated HTML, or logging `document.documentElement.textContent` to the developer tools console. The output for `pdftohtml stegano50.pdf` contained the text too.

Let’s take the `BABA […] AAABB` part and perform the suggested replacements using `tr`:

```bash
$ tr AB .- <<< 'BABA BBB BA BBA ABA AB B AAB ABAA AB B AA BBB BA AAA BBAABB AABA ABAA AB BBA BBBAAA ABBBB BA AAAB ABBBB AAAAA ABBBB BAAA ABAA AAABB BB AAABB AAAAA AAAAA AAAAB BBA AAABB'
-.-. --- -. --. .-. .- - ..- .-.. .- - .. --- -. ... --..-- ..-. .-.. .- --. ---... .---- -. ...- .---- ..... .---- -... .-.. ...-- -- ...-- ..... ..... ....- --. ...--
```

An [online Morse code decoder](http://morsecode.scphillips.com/jtranslator.html) decodes this to:

```
CONGRATULATIONS,FLAG:1NV151BL3M3554G3
```

And indeed, the flag is `1NV151BL3M3554G3`.

## Other write-ups and resources

* <http://www.pwntester.com/blog/2014/04/27/dragonsector-pdf-stegano-50/>
* <http://blog.dul.ac/2014/04/DSCTF14/>
