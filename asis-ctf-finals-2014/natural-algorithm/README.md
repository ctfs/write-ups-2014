# ASIS Cyber Security Contest Finals 2014: Natural algorithm

**Category:** Stego, Recon
**Points:** 150
**Description:**

> Find flag in the [image](sunflower_2b870888a7b24ca81ff00529550ecd5f).

## Write-up

Let’s see what [the provided file](sunflower_2b870888a7b24ca81ff00529550ecd5f) could be:

```bash
$ file sunflower_2b870888a7b24ca81ff00529550ecd5f
sunflower_2b870888a7b24ca81ff00529550ecd5f: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < sunflower_2b870888a7b24ca81ff00529550ecd5f > sunflower`
* `unxz < sunflower_2b870888a7b24ca81ff00529550ecd5f > sunflower`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x sunflower_2b870888a7b24ca81ff00529550ecd5f
```

Let’s find out what the extracted file is:

```bash
$ file sunflower
sunflower: TIFF image data, little-endian
```

Renaming the file to `sunflower.tiff` and opening it in an image viewer reveals a picture of a sunflower (who’d have thought?!). [A reverse image search](https://goo.gl/XVhPvX) shows lots of results regarding [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number) in nature.

Maybe we should read each byte from the file whose offset corresponds to a Fibonacci number? Let’s see what happens if we do that:

```python
#!/usr/bin/env python
# coding=utf-8
import os

file_path = 'sunflower.tiff'
file_size = os.stat(file_path).st_size
f = open(file_path, 'rb')

current_offset = 1
next_offset = 1
result = ''
while next_offset <= file_size:
  current_offset, next_offset = next_offset, current_offset + next_offset
  f.seek(current_offset)
  result += f.read(1)
print result
```

Running the above Python script prints:

```
I*. ASIS_md5(Fib[10^6])
```

So, we need to figure out what the `10^6`th Fibonacci number is, then calculate its MD5 hash. Luckily, we don’t have to compute this number ourselves — there is [a website dedicated to it](http://www.upl.cs.wisc.edu/~bethenco/fibo/)!

Copying the number from there and removing all line breaks should result in [a very long string](https://gist.githubusercontent.com/anonymous/e787672f2f174db5e9cd/raw/2dca7ad19e560fafb5f5d4f8a1246a983891cf16/fibonacci-1000000.txt) with MD5 hash `e73d27576c4f40d414d9f666c3c79554`.

The flag is `ASIS_e73d27576c4f40d414d9f666c3c79554`.

## Other write-ups and resources

* none yet
