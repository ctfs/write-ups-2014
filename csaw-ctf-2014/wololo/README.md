# CSAW CTF 2014: wololo

**Category:** Reverse Engineering
**Points:** 300
**Description:**

> ```bash
> nc 54.164.98.39 2510
> ```
>
> Written by RyanWithZombies
>
> Hint:
>
> ```c
> typedef struct
> {
>         uint32_t magic;
>         uint32_t version;
>         uint16_t num_cols;
>         uint16_t num_rows;
> } header_t;
>
> typedef struct
> {
>         uint8_t type;
>         char name[16];
> } col_t;
>
> /*
>  * Column types:
>  *   * 0 = 8bit integer
>  *   * 1 = 16bit integer
>  *   * 2 = 32bit integer
>  *   * 3 = 64bit integer
>  *   * 4 = 8byte string
>  *   * 5 = 16byte string
>  *   * 6 = 32byte string
>  *   * 7 = unix timestamp encoded as a 32bit integer
>  *
>  */
> ```
>
> [wololo.lst.xz](wololo.lst.xz)

## Write-up

Let’s run the command provided in the challenge description.

```bash
$ nc 54.164.98.39 2510

I'm ready to accept your input file!

Run this with: python wololo_x.py hostname port file_to_submit

#!/usr/bin/env python

import sys, socket, struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
print s.recv(1024)

contents = open(sys.argv[3], "rb").read()
s.send(struct.pack("<I", len(contents)) + contents)

print "The challenge server says: ", s.recv(1024)
```

Okay, let’s store the above Python script to [a file named `wololo_x.py`](wololo_x.py) and try to submit a random test file to the server:

```bash
$ python wololo_x.py 54.164.98.39 2510 some-random-test-file
```

The server responds:

```
The challenge server says:  Sorry, your file did not pass all the checks.
```

(TODO)

## Other write-ups and resources

* [Exploit written in Python by @ebeip90](https://gist.github.com/ebeip90/d167b9a52cb55fbffeb2#file-wololo-py)
* <http://tasteless.se/2014/09/csaw-2014-quals-wololo-rev300/>
