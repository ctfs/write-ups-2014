# SECCON CTF 2014: Get the key.txt

**Category:** Forensics
**Points:** 100
**Description:**

> [`forensic100.zip`](forensic100.zip)

## Write-up

Let’s extract [the provided ZIP file](forensic100.zip):

```bash
$ file forensic100.zip
forensic100.zip: Zip archive data, at least v2.0 to extract

$ unzip forensic100.zip
Archive:  forensic100.zip
  inflating: forensic100
```

The extracted file is filesystem data:

```bash
$ file forensic100
forensic100: Linux rev 1.0 ext2 filesystem data
```

Let’s try to `mount` it.

```
$ mkdir /tmp/forensic100

$ cd /tmp/forensic100

$ mount -o loop forensic100 /tmp/forensic100

$ ls
1    116  133  150  168  185  201  219  236  33  50  68  85
10   117  134  151  169  186  202  22   237  34  51  69  86
100  118  135  152  17   187  203  220  238  35  52  7   87
101  119  136  153  170  188  204  221  239  36  53  70  88
102  12   137  154  171  189  205  222  24   37  54  71  89
103  120  138  155  172  19   206  223  240  38  55  72  9
104  121  139  156  173  190  207  224  241  39  56  73  90
105  122  14   157  174  191  208  225  242  4   57  74  91
106  123  140  158  175  192  209  226  243  40  58  75  92
107  124  141  159  176  193  21   227  244  41  59  76  93
108  125  142  16   177  194  210  228  25   42  6   77  94
109  126  143  160  178  195  211  229  26   43  60  78  95
11   127  144  161  179  196  212  23   27   44  61  79  96
110  128  145  162  18   197  213  230  28   45  62  8   97
111  129  146  163  180  198  214  231  29   46  63  80  98
112  13   147  164  181  199  215  232  3    47  64  81  99
113  130  148  165  182  2    216  233  30   48  65  82  lost+found
114  131  149  166  183  20   217  234  31   49  66  83
115  132  15   167  184  200  218  235  32   5   67  84
```

It worked! That’s a lot of files. Let’s take the hint from the challenge title and look for occurrences of `key.txt` within those files.

```bash
$ grep -r 'key.txt' .
Binary file ./1 matches
```

Let’s take a closer look at file `1`:

```bash
$ file 1
1: gzip compressed data, was "key.txt", from Unix, last modified: Wed Oct  1 02:00:52 2014
```

Oh, it’s gzip-compressed data. Let’s decompress it:

```bash
$ gunzip < 1
SECCON{@]NL7n+-s75FrET]vU=7Z}
```

The flag is `SECCON{@]NL7n+-s75FrET]vU=7Z}`.

## Other write-ups and resources

* <http://icheernoom.blogspot.de/2014/12/seccon-ctf-2014-get-keytxt-forensics.html>
* [Indonesian](http://www.hasnydes.us/2014/12/get-key-txt-seccon-ctf-writeups-100pts/)
