# DEFKTHON CTF: Miscellaneous 200

**Description:**

> [Flag is Here!](flag.txt)

## Write-up

The provided `flag.txt` file contains tuples of three comma-separated values on each line. This looks like an image with given RGB values.

In total, there are 61366 lines:

```bash
$ wc -l flag.txt
61366 flag.txt
```

The dimensions of the image are dividers of this number, so possibly: 1, 2, 61, 122, 503, 1006, 30683, 61366. The most likely image size is 122×503px or 503×112px.

### Solution 1: using PPM

The easiest way to convert this text file into an image, is by converting it to the PPM format with the following header:

```ppm
P3
122 503
255
```

…then followed by the contents of `flag.txt`, with any commas replaced by spaces. The result is [`flag.ppm`](flag.ppm).

Let’s convert it to PNG, and flip + rotate it to make it easier to read:

```bash
$ convert -flip -rotate 90 flag.ppm flag.png
```

This results in [the following image](flag.png):

![flag{ youc@n'tseeme }](flag.png)

### Solution 2: using Python and PIL

Using some string parsing and the Python Imaging Library (PIL), an image can be drawn pixel by pixel from the given RGB values.  The dimensions were the tricky part, as using exact multiples overflowed the program, so using one set value for the width and a very high number for the height, the image was drawn well enough.

```python
from PIL import Image
import numpy

pixels = open("flag.txt").read().split("\n")
del pixels[-1]

myPixelsArray = ()

for x in pixels:
  array = x.split(",")
  array = tuple([int(w) for w in array])
  myPixelsArray += array

myImage = Image.new("RGB", (122, 503))

myImage.putdata(myPixelsArray)

myImage.save("flag.jpg")
```

The image, when cropped and flipped, shows the following:

![flag{ youc@n'tseeme }](flag.jpg)

## Other write-ups and resources

* <http://blog.0xdeffbeef.com/2014/03/defkthon-ctf-2014-flag-is-here-misc-200.html>
* <http://www.cravetocode.com/2014/03/defkthon-ctf-misc-200-writeup.html>
* <http://tasteless.eu/2014/03/defkthon-ctf-2014-rev200-misc200-recon200-misc300/>
* <https://shankaraman.wordpress.com/2014/03/05/defkthon-ctf-misc-200-writeup/>
* [Russian](http://reu.org.ua/ctf/write-up-defkthon-ctf-2014-misc-200.html)
