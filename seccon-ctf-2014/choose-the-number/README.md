# SECCON CTF 2014: Choose the number

**Category:** Programming
**Points:** 100
**Description:**

> ```bash
> nc number.quals.seccon.jp 31337
> ```

## Write-up

This service gives you a list of numbers, and then asks for either the lowest or the highest of those numbers. If you enter the correct answer, the next challenge appears.

```bash
$ nc number.quals.seccon.jp 31337
0, 7, -3
The maximum number? 7
6, 0, -3, -2
The maximum number? 6
-8, 3, 0, 6, 4
The minimum number? -8
2, 0, -8, 2, 5, 2
The maximum number?
```

We wrote [a Python script to automate this](solve.py), and let it run for a while. After answering 100 challenges correctly, the flag is revealed:

```
 -4221710437, -1740702929, 4270517397, 3209397296, 3762024025, -3672989483, -775093555, 4151733183, 3564119176, -2899783113, -3331662677, 642770555, -3121798555, 1288976181, -3587672601, 2905985917, 2137540564, 1172635558, -1479609079, -1248372983, 3873677181, 1248052749, -1034576168, 2036474576, -253149619, -2392684096, -1930807573, -2317594216, 929234744, -1670667531, -1628006672, 879994792, 1969573571, -1305518363, -1355550455, 1095362934, -124373352, -1807675908, 3878897952, -1837056383, -2612347417, -1268914355, 4050965082, 1631467597, 2186132639, -2873319762, 2416444358, 3467519746, 1294589509, 690827023, -1648894301, 3245051371, -4125602438, 2445841557, -47857822, -148422805, 1594344784, -2702599035, -2113258438, 439412574, -3648358307, 701139315, 2674841307, -276835850, 2008480906, -742379070, -854097465, 2338492179, 653621662, 3204170814, -4292552234, -592497316, -2541019100, -1497564068, -1732032680, 188766876, -2759314033, 1756911371, -2155898580, 1151212441, -2647634085, 3941284198, -1621905813, 3066978392, 2108513714, -2592441740, -2432239477, 582366717, 151030349, -3056239567, -3323966535, 3134812599, -2106237224, -3366016099, -3040745768, -959614841, 3068410499, -3895262470, 784215697, -2397024752, 2321915702
The maximum number?
>>> 4270517397
 Congratulations!
The flag is SECCON{Programming is so fun!}
```

The flag is `SECCON{Programming is so fun!}`.

## Other write-ups and resources

* <http://blogs.univ-poitiers.fr/e-laize/2014/12/07/seccon-2014-quals-prog-choose-number/>
* <https://github.com/S42X/CTF/blob/master/SECCON/ChooseTheNumber.md>
* <https://shankaraman.wordpress.com/2014/12/07/seccon-2014-writeups-networking-100-and-programming-100/>
* <http://icheernoom.blogspot.de/2014/12/seccon-ctf-2014-choose-number.html>
* <https://rzhou.org/~ricky/seccon2014/number/test.py>
* <https://github.com/rezk2ll/SECCON_2014_Programming100/blob/master/prog100.py>
* [Portuguese](https://ctf-br.org/wiki/seccon/seccon2014/p100-choose-the-number/)
* [Indonesian](http://www.hasnydes.us/2014/12/choose-number-100pts-seccon-ctf-2014/)
