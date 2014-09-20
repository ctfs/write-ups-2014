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

(TODO)

## Other write-ups

* none yet
