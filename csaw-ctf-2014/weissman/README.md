# CSAW CTF 2014: weissman

**Category:** Reverse Engineering
**Points:** 300
**Description:**

> Extract the key!
>
> Written by RyanWithZombies
>
> Update: The key is not `flag{ don't trust the Cheshire cat!! he works for the Queen of Hearts }`. Sorry about that. It's an artifact from an easier version of this challenge. You need to extract `key.jpg`.
>
> HINT:
>
> CSAWLZ is a completely custom format! You won't find decompressing tools on the internet. We made it just for you. :)
>
> ```c
> typedef struct _hdr {
>     uint8_t magic[8];
>     uint32_t version;
>     uint32_t num_files;
> } hdr;
>
> typedef struct _entry {
>     uint32_t magic;
>     uint32_t compressed_size;
>     uint32_t uncompressed_size;
>     uint8_t filename[32];
> } entry;
> ```
>
> [weissman.csawlz](weissman.csawlz)

## Write-up

Here is a [Java-based solution](CSAWlz.java) to this challenge.

During the CTF, it seems that most (probably all) of the people who solved it, didn’t completely decompress the files contained within the archive, but were able to get the important file (`key.jpg`) readable enough simply by filling the space required with zeros, as described in the link below.

After the CTF was complete, I asked to author (RyanWithZombies) if he was going to do a write-up, but he said he wasn’t and linked me to the C++ source he used to compress the archive (https://gist.github.com/withzombies/909b403852ea1e31f553). I was able to port the decompressing and hashing code to Java and incorporate it into the code I wrote during the CTF. Our team didn’t actually get the key in time (oh well) but I was interested enough to keep poking at this until I got it to work.

Roughly, the process of extracting a single file is this:

- first, create a _hashmap_ to store uncompressed data blocks
- read the first byte from the _input_, which is a _control byte_

Then in a loop, do this:

- `control_byte >> 1`  to extract the _size_ of the current data block
- `control_byte & 0b00000001) != 0b00000001` to determine if the block is `compressed` or not (if the statement evaluates to `true`, the block is compressed)

If the block is not `compressed`:

- read `size` number of bytes from the `input` and store them in a `buffer`.
- create a `hash` of the first 4 bytes in the buffer
- store the buffered bytes in the `hashmap` using the `hash` as the key
- write the `buffer` to `output`
- read the next `control_byte` if it exists and restart the loop

If the block is _compressed_:

- read two bytes from the `input`; these bytes are the `hash`
- using the `hash` as the key, get the bytes stored in the `hashmap`
- read `size` number of bytes from the bytes you just retrieved from the hashmap into a `buffer`
- write the bytes in the `buffer` to the `output`
- read the next `control_byte` if it exists and restart the loop

When you find that the next `control_byte` doesn’t exist, you are done and can write the `output` to disk.

As stated, this is a very rough outline of what is actually going on — check out the [`CSAWlz.java`](CSAWlz.java) file for a better understanding of exactly what happens during decompressing.

Thanks to RyanWithZombies for an interesting challenge!

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/09/csaw14-weissman-writeup.html>
