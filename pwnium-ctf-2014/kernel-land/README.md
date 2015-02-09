# Pwnium CTF 2014: Kernel Land

**Category:** Reverse
**Points:** 150
**Description:**

> The third Tick gives you the answer ;) [http://41.231.53.40/kernel](kernel)

## Write-up

The algorithm is described in `timer_tick` and the data is in the global variable `flag`.

Calculate the flag as follows:

```python
flag_data =[
0x49, 0x74, 0x6F, 0x66, 0x72, 0x6A, 0x78, 0x62, 0x32, 0x60, 0x2E,
0x2E, 0x63, 0x2E, 0x32, 0x2E, 0x36, 0x30, 0x33, 0x31, 0x5D, 0x67,
0x36, 0x62, 0x31, 0x67, 0x67, 0x30, 0x5E, 0x29, 0x62, 0x31, 0x31,
0x63, 0x62, 0x5E, 0x5E, 0x2D, 0x5D, 0x7A]

for i in range(1, 4):
    for x in range(len(flag_data)):
        flag_data[x] = ((flag_data[x]^i)+1) % 256

print "".join(map(chr, flag_data))
```

## Other write-ups and resources

* <http://blog.randomguys.fr/pwnium2014-kernel-land.html>
* <https://in3o.wordpress.com/2014/07/06/pwnium-ctf-2014-reverse-150-kernel-land/>
