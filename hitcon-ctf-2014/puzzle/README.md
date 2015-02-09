# HITCON CTF 2014: puzzle

**Category:** Puzzle
**Points:** 150
**Description:**

> [https://raw.githubusercontent.com/hitcon2014ctf/ctf/master/puzzle-81c5e9bdb219efbe4eb9b194fb33f7e6.jpg](puzzle-81c5e9bdb219efbe4eb9b194fb33f7e6.jpg)
> [https://dl.dropbox.com/s/wh0uset031ivgsq/puzzle-81c5e9bdb219efbe4eb9b194fb33f7e6.jpg](puzzle-81c5e9bdb219efbe4eb9b194fb33f7e6.jpg)

**Hint:**

> If you have found the flag but it contains characters hard to recognize, pm admin and get correct flag.
>
> Q: Hey I can see "HITCON{" prefix, is that enough?
> A: No, you can and have to extract more.
>
> Flag Format: `HITCON{lllluuul_luul_udd}`
> lowercase / uppercase / digit

## Write-up

Let’s start this challenge by taking a closer look to the image in a hex editor. There are a few things that should get your attention.

* There are two image headers: a JFIF and an EXIF header
* There are multiple JFXX thumbnails

If we take the EXIF data from the image and put that in a new one we get [the following image](ExifImage.jpg). So there must be something hidden in the first part of the image. Since there are multiple thumbnails and the title of the challenge is puzzle I figured we had to extract those thumbnails. A little bit [research on JPEG headers](http://blog.bfitz.us/?p=289) was useful. This enabled me to write [a script for extracting the thumbnails](puzzlesolver.py). This script extracts and creates 100 images.

The second stage of the challenge is literally a puzzle. You got 100 images and you have to puzzle them together. I also wrote [a script to puzzle them together](puzzlesolver_part2.py) however this script does not bruteforce the solution, since there are 5050 different possibilities and I didn’t want to end up with 5050 images in my folder.

```py
# put all the images in the new image
def solve_im(new_im, arr):
    for i in range(100):
        name = str(i+1) + ".jpg"
        im = Image.open(name)
        new_im.paste(im, ((arr.index(i)%10)*128,arr.index(i)/10*96))
```

As you can see you can give an array as argument to the function and it places the images accordingly.

After puzzling the real image together we can see a piece of the flag. Now it is a matter of manipulating the image untill you see the full flag. I used photoshop and the calculations function. After manipulating for a while and using the hint `HITCON{lllluuul_luul_udd}` where `l` is lowercase and `u` is uppercase I came to the following flag: `HITCON{mounTAIn_jPEg_I01}`.

## Other write-ups and resources

* <http://blog.squareroots.de/en/2014/08/hitcon-ctf-2014-puzzle/>
