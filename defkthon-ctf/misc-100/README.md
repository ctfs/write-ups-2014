# DEFKTHON CTF: Miscellaneous 100

**Description:**

> He is so FAT.
> Flag is the md5 of a windows command with numericals in it.

## Write-up

Apparently the expected answer was `289cca92d315659c671f51ad8e0f06d3`, the MD5 hash of `8dot3name`. This is not really a Windows command, though – although it can be used as an argument to [`fsutil`](http://technet.microsoft.com/en-us/library/ff621566.aspx).

## Other write-ups and resources

* none yet
