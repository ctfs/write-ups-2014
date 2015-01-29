# Ghost in the Shellcode 2014: Revenge of Imgception

**Category:** Forensics
**Points:** 300
**Description:**

> Find the key. [Link](https://2014.ghostintheshellcode.com/roi-0252563f02b4e004978185322f1766b0/index.html)

## Write-up

The HTML source for that link is:

```
<html
<head>
  <script>
    function get_image() {
      var i = new Image();
      var num = parseInt((Math.random() * 50), 10) +1
      i.src = './' + num;
      document.getElementById('t').appendChild(i);
    }
  </script>
</head>
<body onload="get_image()">
  <div id="t"></div>
</body>
</html>
```

The `get\_image` function generates a number from 1 to 50, and then uses that as part of the URL for an image. The image files don’t have an extension, but looking at the headers it’s obvious they’re JPEGs. So, let’s download them all:

```bash
$ for i in {1..50}; do curl -# "https://2014.ghostintheshellcode.com/roi-0252563f02b4e004978185322f1766b0/${i}" > "${i}.jpg"; done
```

The clue to the next step is hidden as base64-encoded data in the comment fields (`\xFF\xFE`) of these images. The number of comment fields is variable because they have a maximum size of `65535` (`0xFFFF`).

The extracted data is an animated GIF file. The next stage is hidden in a set of comment extensions as binary data. The number of comment extensions is variable depending on the size of the next stage.

The extracted data is is a zip file full of PNG images. The next stage is spread among them. Each PNG has a custom chunk marked with a `icTf` header. Each chunk begins with 3 bytes of the order string (`'ThankYouMarioButOurPrincessIsInAnotherCastle' * 20`) followed by a null byte, followed by binary data. The binary data chunks from each file must be concatenated together in the order given by the order string. The entirety of the order string may not be used, as the zip contains a variable number of files.

That results in a new file, which is a floppy disk image containing a Super Mario Brothers ROM image for the Nintendo Entertainment System. This can be played in [the FCEUX emulator](http://www.fceux.com/web/home.html), but that’s a red herring. Instead, the key to the next stage has been concatenated to the end of the ROM, and is marked with `'GITS' * 512`.

The next file is an ISO image with a hidden directory. When mounted with default (Linux) options, the only apparent file is a JPEG image. However, when mounted with the `--no-joliet` option, the next stage becomes apparent.

The file is a multi-page TIFF image with broken file magic. The file magic is `\x49\x4d\x2a\x2a`. The TIFF file header indicates whether the image is little endian or big endian by the first two bytes being either `\x49\x49` (little) or `\x4d\x4d` (big). The next two bytes are similarly arranged, either `\x2a\x00` (little) or `\x00\x2a` (big). The correct file header for this image is `\x49\x49\x2a\x00`. Once the header is fixed, the image contains three images - one world 7-1 image and two apparently identical world 8-1 images that constitute the next stage.

The files are two apparently identical greyscale BMP images. The images are not, however, identical. The final image is steganographically hidden in the delta between color byte values. By subtracting the byte values in one file from the corresponding byte in the other, some bytes result in a value between `-8` and `+7`. Each value represents a single nibble of the final image.

The final image contains a congratulatory message and the key: `K00pas@llth3w@yd0wn`.

## Other write-ups and resources

* <http://pastebin.com/q8Lf8M0w>
