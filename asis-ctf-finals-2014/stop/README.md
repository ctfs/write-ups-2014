# ASIS Cyber Security Contest Finals 2014: Stop!

**Category:** Stego, Crypto
**Points:** 150
**Description:**

> In this [file](stop_53e41e604422d4fa824490ca852dfecb), flag is hidden, find it! and don't stop!

## Write-up

Let’s see what [the provided file](stop_53e41e604422d4fa824490ca852dfecb) could be:

```bash
$ file stop_53e41e604422d4fa824490ca852dfecb
stop_53e41e604422d4fa824490ca852dfecb: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < stop_53e41e604422d4fa824490ca852dfecb > stop`
* `unxz < stop_53e41e604422d4fa824490ca852dfecb > stop`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x stop_53e41e604422d4fa824490ca852dfecb
```

Let’s find out what the extracted file is:

```bash
$ file stop
stop: MPEG sequence, v2, program multiplex
```

Renaming the file to `stop.mpeg` allows us to open it in our video player of choice.

The movie features a stop sign (an octagon) that rotates to 8 different positions:

![](example-frame.jpg)

Some frames have a dot in the corner to the upper left of the ‘STOP’ text (like in the above example), others don’t.

So, in total there are 16 different kinds of images used as as frame.

Let’s extract all frames:

```bash
$ ffmpeg -i stop.mpeg -ss 00:00:00 -t 60 -qscale 0 -f image2 frame-%04d.png
```

Now we go through each of the frames, starting at `frame-0000.png`, and assign a hexadecimal digit every time the image changes to another one of the 16 variations, like so:

* STOP with no rotation and no dot: `0`
* STOP with 135° rotation and no dot: `1`

(TODO)

## Other write-ups and resources

* none yet
