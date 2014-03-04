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

* none yet
