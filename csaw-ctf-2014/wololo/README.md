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

(TODO)

## Other write-ups

* none yet
