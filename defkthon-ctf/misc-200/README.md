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

## Other write-ups

### Using Python and PIL

Using some string parsing and the Python Imaging Library (PIL), an image can be drawn pixel by pixel from the given RGB values.  The dimensions were the tricky part, as using exact multiples overflowed the program, so using one set value for the width and a very high number for the height, the image was drawn well enough.

```
from PIL import Image
import numpy
 
flag = open("flag.txt")
 
pixels = flag.read().split("\n")
del pixels[-1]
 
myPixelsArray = ()
 
for x in pixels:
    array = x.split(",")
    array = tuple([int(w) for w in arrayer])
    myPixelsArray += array
 
myImage = Image.new("RGB", (122, 10000))
 
myImage.putdata(myPixelsArray)
 
myImage.save("image.jpeg")
```

The image, when cropped and flipped, shows the following:

![flag{ youc@n'tseeme }](image.jpeg)
