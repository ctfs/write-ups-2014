# DEFKTHON CTF: Miscellaneous 200

**Description:**

> [Flag is Here!](flag.txt)

## Write-up

The given textfile contains tuples of 3 comma-separated values on each line. This looks like an image with given RGB values.

In total, there are 61366 lines:

```bash
$ wc -l flag.txt 
   61366 flag.txt
```

The dimensions of the image are dividers of this number, so possibly: 1, 2, 61, 122, 503, 1006, 30683, 61366.
The most likely image size is 122x503 or 503x112.

The easiest way to convert this textfile into an image, is by converting it to PPM format with the following header:

```bash
P3
122 503
255
```

Then followed by the contents of flag.txt, but commas replaced by spaces.
[flag.ppm](flag.ppm)

Converting to PNG for viewing (and flipping + rotating):
```bash
convert -flip -rotate  90 flag.ppm flag.png
```

results in 

![](flag.png)

## Other write-ups

* none yet
