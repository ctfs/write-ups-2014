# HITCON CTF 2014: 24

**Category:** Game
**Points:** 256
**Description:**

> Let’s play a game!
>
> ```bash
> $ nc 210.65.89.59 2424
> ```

## Write-up

```bash
$ nc 210.65.89.59 2424
===================================================
===           Welcome to the 24 game!           ===
=== You have 2 minutes to answer all questions. ===
===================================================

Question (1 of 24): [9, 1, 3, 2]
Answer: 9,1,3,2
ERROR!!! Answer should match [-+*/0-9()]+
```

Okay, so we’re supposed to enter digits and some operators only.

```bash
$ nc 210.65.89.59 2424
===================================================
===           Welcome to the 24 game!           ===
=== You have 2 minutes to answer all questions. ===
===================================================

Question (1 of 24): [11, 9, 3, 11]
Answer: 11+9+3+11
ERROR!!! abs(eval(answer) - 24) >= 1e-15
```

Oh, and our input must evaluate to `24`. That makes sense.

```bash
$ nc 210.65.89.59 2424
===================================================
===           Welcome to the 24 game!           ===
=== You have 2 minutes to answer all questions. ===
===================================================

Question (1 of 24): [5, 4, 2, 2]
Answer: 5*4+2+2
Great!
```

Some further testing confirms that this is a Python script:

```bash
$ nc 210.65.89.59 2424
===================================================
===           Welcome to the 24 game!           ===
=== You have 2 minutes to answer all questions. ===
===================================================

Question (1 of 24): [8, 9, 2, 3]
Answer: 8-9-2-3-
Traceback (most recent call last):
  File "/home/twenty-four/server.py", line 54, in <module>
    Main()
  File "/home/twenty-four/server.py", line 40, in Main
    if abs(eval(ans) - 24) >= 1e-15:
  File "<string>", line 1
    8-9-2-3-
           ^
SyntaxError: unexpected EOF while parsing
```

This is useful, because it means we’re not limited to the `-`, `+`, `*`, and `/` operators — we can use Python’s `**` and `//` too!

We have to solve 24 of these puzzles in just 2 minutes. Let’s write a script for it.

(TODO)

```
…

Question (23 of 24): [6, 11, 8, 5]
Answer:
('6', '11', '8', '5')
((6+11)//5)*8
Great!


Question (24 of 24): [13, 4, 1, 13]
Answer:
('13', '4', '1', '13')
13//(13**-(4**-1))
Good job! Here's your flag: HITCON{24_GAme_15_FUN}
```

The flag is `HITCON{24_GAme_15_FUN}`.

## Other write-ups and resources

* <https://gist.github.com/gnomus/4a119910a616b703620a>
* <https://gist.github.com/csferng/cfc18104d9adfa25224f>
