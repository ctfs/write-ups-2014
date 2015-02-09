# NoConName 2014 Quals: inMISCible

**Category:** Misc
**Points:** 200
**Description:**

No hints :( just go and get the flag.

## Write-up

The file has no extension, but using the "file" command we find out it's a gzip archive and the original name is "ctf.py.gz".

```
$ file ctf
ctf: gzip compressed data, was "ctf.py", from Unix, last modified: Thu Jul 24 18:42:37 2014
$ mv ctf ctf.py.gz
$ gzip -d ctf.py.gz
$ file ctf.py
ctf.py: Python script, ASCII text executable
```

The source code of this Python file is ROT-13 encoded.

```
$ head ctf.py -n 2
#!/usr/bin/env python
# -*- coding: rot13 -*-
```

And when we run it we get the following output:

```
$ python ctf.py
Nope!
```

So we'll have to look at the code to see what's wrong. Let's decode it:

```
$ python
Python 2.7.3 (default, Mar 13 2014, 11:03:55)
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> d=open("ctf.py","rU").read().decode("rot13")
>>> d=d.replace('.decode("ebg13")', '')
>>> open("ctf_decoded.py", "w").write(d)
>>> exit()
```

Now we can read the source.

```
#!/hfe/ova/rai clguba
# -*- pbqvat: ebg13 -*-
import os
import marshal
import new

global flag

def f():
    global flag
    flag = "Nope!"

bytecode = """
YwAAAAAAAAAAAwAAAEAAAABzlwAAAGQAAGQBAGwAAG0BAFoBAAFkAABkAgBsAgBtAwBaAwABZQMA
ZAMAZAQAgwIAZAUAawIAcpMAZAYAYQQAdAQAZAcAN2EEAHQEAGQIADdhBAB0BABkCQA3YQQAdAQA
agUAZAoAZAQAgwIAYQQAdAQAagYAZAsAgwEAYQQAZAwAZQEAdAQAgwEAagcAgwAAF2EEAG4AAGQN
AFMoDgAAAGn/////KAEAAABzBAAAAHNoYTEoAQAAAHMGAAAAZ2V0ZW52cwsAAABOT19DT05fTkFN
RXMAAAAAcwEAAABZczEAAAAgNTcgNjggNjEgNzQgMjAgNjkgNzMgMjAgNzQgNjggNjUgMjAgNjEg
NjkgNzIgMmQgczEAAAAgNzMgNzAgNjUgNjUgNjQgMjAgNzYgNjUgNmMgNmYgNjMgNjkgNzQgNzkg
MjAgNmYgczEAAAAgNjYgMjAgNjEgNmUgMjAgNzUgNmUgNmMgNjEgNjQgNjUgNmUgMjAgNzMgNzcg
NjEgcxAAAAAgNmMgNmMgNmYgNzcgM2YgcwEAAAAgcwMAAABoZXhzAwAAAE5DTk4oCAAAAHMHAAAA
aGFzaGxpYnMEAAAAc2hhMXMCAAAAb3NzBgAAAGdldGVudnMEAAAAZmxhZ3MHAAAAcmVwbGFjZXMG
AAAAZGVjb2RlcwkAAABoZXhkaWdlc3QoAAAAACgAAAAAKAAAAABzCAAAADxzdHJpbmc+cwgAAAA8
bW9kdWxlPgIAAABzEgAAABABEAEVAgYBCgEKAQoBEgEPAQ==
"""

if __name__ != "__main__":
    codeobj = marshal.loads(bytecode)
    f = new.function(codeobj, globals(), "f", None, None)

f()

print flag
```

The first two lines are wrong, but it doesn't matter, the script will run anyway.

So, first there are a couple of imports, then a global variable called "flag" is defined (we'll assume the flag will be there at some point), a function called "f" sets it as "Nope!", thereś another variable called "bytecode" with some binary data, a block of code that can only be executed when importing the module (not when running it as a script), then the "f" function is called and the "flag" variable is printed out.

Clearly the key part here is the binary blob and the conditional block. Let's run the script as an imported module to get into the conditional block:

```
$ python
Python 2.7.3 (default, Mar 13 2014, 11:03:55)
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import ctf_decoded.py
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ctf_decoded.py", line 26, in <module>
    codeobj = marshal.loads(bytecode)
ValueError: bad marshal data (unknown type code)
>>>
```

Now we're getting a different error message. Let's take a closer look at that conditional block. We see the variable "bytecode" is decoded using the "marshal" module, we now we know that blob contains Python serialized data. Next a new function is created in runtime using the data from the blob, hence the name of the variable "bytecode" - the blob is Python bytecode. But this cannot work, the blob seems to be encoded using base64. Let's fix the script by changing this line:

```
    codeobj = marshal.loads(bytecode)
```

To this:

```
    codeobj = marshal.loads(bytecode.decode("base64"))
```

And run it again:

```
>>> import ctf_decoded
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ctf_decoded.py", line 31, in <module>
    print flag
NameError: global name 'flag' is not defined
```

Something else is broken! This time we'll have to look at that mystery bytecode, for which we have no sources. But we have the "dis" module to disassemble the bytecode, it comes with Python itself.


```
>>> bytecode = """
... YwAAAAAAAAAAAwAAAEAAAABzlwAAAGQAAGQBAGwAAG0BAFoBAAFkAABkAgBsAgBtAwBaAwABZQMA
... ZAMAZAQAgwIAZAUAawIAcpMAZAYAYQQAdAQAZAcAN2EEAHQEAGQIADdhBAB0BABkCQA3YQQAdAQA
... agUAZAoAZAQAgwIAYQQAdAQAagYAZAsAgwEAYQQAZAwAZQEAdAQAgwEAagcAgwAAF2EEAG4AAGQN
... AFMoDgAAAGn/////KAEAAABzBAAAAHNoYTEoAQAAAHMGAAAAZ2V0ZW52cwsAAABOT19DT05fTkFN
... RXMAAAAAcwEAAABZczEAAAAgNTcgNjggNjEgNzQgMjAgNjkgNzMgMjAgNzQgNjggNjUgMjAgNjEg
... NjkgNzIgMmQgczEAAAAgNzMgNzAgNjUgNjUgNjQgMjAgNzYgNjUgNmMgNmYgNjMgNjkgNzQgNzkg
... MjAgNmYgczEAAAAgNjYgMjAgNjEgNmUgMjAgNzUgNmUgNmMgNjEgNjQgNjUgNmUgMjAgNzMgNzcg
... NjEgcxAAAAAgNmMgNmMgNmYgNzcgM2YgcwEAAAAgcwMAAABoZXhzAwAAAE5DTk4oCAAAAHMHAAAA
... aGFzaGxpYnMEAAAAc2hhMXMCAAAAb3NzBgAAAGdldGVudnMEAAAAZmxhZ3MHAAAAcmVwbGFjZXMG
... AAAAZGVjb2RlcwkAAABoZXhkaWdlc3QoAAAAACgAAAAAKAAAAABzCAAAADxzdHJpbmc+cwgAAAA8
... bW9kdWxlPgIAAABzEgAAABABEAEVAgYBCgEKAQoBEgEPAQ==
... """
>>> import marshal
>>> import dis
>>> codeobj = marshal.loads(bytecode.decode("base64"))
>>> dis.disassemble(codeobj)
  2           0 LOAD_CONST               0 (-1)
              3 LOAD_CONST               1 (('sha1',))
              6 IMPORT_NAME              0 (hashlib)
              9 IMPORT_FROM              1 (sha1)
             12 STORE_NAME               1 (sha1)
             15 POP_TOP

  3          16 LOAD_CONST               0 (-1)
             19 LOAD_CONST               2 (('getenv',))
             22 IMPORT_NAME              2 (os)
             25 IMPORT_FROM              3 (getenv)
             28 STORE_NAME               3 (getenv)
             31 POP_TOP

  4          32 LOAD_NAME                3 (getenv)
             35 LOAD_CONST               3 ('NO_CON_NAME')
             38 LOAD_CONST               4 ('')
             41 CALL_FUNCTION            2
             44 LOAD_CONST               5 ('Y')
             47 COMPARE_OP               2 (==)
             50 POP_JUMP_IF_FALSE      147

  6          53 LOAD_CONST               6 (' 57 68 61 74 20 69 73 20 74 68 65 20 61 69 72 2d ')
             56 STORE_GLOBAL             4 (flag)

  7          59 LOAD_GLOBAL              4 (flag)
             62 LOAD_CONST               7 (' 73 70 65 65 64 20 76 65 6c 6f 63 69 74 79 20 6f ')
             65 INPLACE_ADD
             66 STORE_GLOBAL             4 (flag)

  8          69 LOAD_GLOBAL              4 (flag)
             72 LOAD_CONST               8 (' 66 20 61 6e 20 75 6e 6c 61 64 65 6e 20 73 77 61 ')
             75 INPLACE_ADD
             76 STORE_GLOBAL             4 (flag)

  9          79 LOAD_GLOBAL              4 (flag)
             82 LOAD_CONST               9 (' 6c 6c 6f 77 3f ')
             85 INPLACE_ADD
             86 STORE_GLOBAL             4 (flag)

 10          89 LOAD_GLOBAL              4 (flag)
             92 LOAD_ATTR                5 (replace)
             95 LOAD_CONST              10 (' ')
             98 LOAD_CONST               4 ('')
            101 CALL_FUNCTION            2
            104 STORE_GLOBAL             4 (flag)

 11         107 LOAD_GLOBAL              4 (flag)
            110 LOAD_ATTR                6 (decode)
            113 LOAD_CONST              11 ('hex')
            116 CALL_FUNCTION            1
            119 STORE_GLOBAL             4 (flag)

 12         122 LOAD_CONST              12 ('NCN')
            125 LOAD_NAME                1 (sha1)
            128 LOAD_GLOBAL              4 (flag)
            131 CALL_FUNCTION            1
            134 LOAD_ATTR                7 (hexdigest)
            137 CALL_FUNCTION            0
            140 BINARY_ADD
            141 STORE_GLOBAL             4 (flag)
            144 JUMP_FORWARD             0 (to 147)
        >>  147 LOAD_CONST              13 (None)
            150 RETURN_VALUE
```

This looks like an important part:

```
  3          16 LOAD_CONST               0 (-1)
             19 LOAD_CONST               2 (('getenv',))
             22 IMPORT_NAME              2 (os)
             25 IMPORT_FROM              3 (getenv)
             28 STORE_NAME               3 (getenv)
             31 POP_TOP

  4          32 LOAD_NAME                3 (getenv)
             35 LOAD_CONST               3 ('NO_CON_NAME')
             38 LOAD_CONST               4 ('')
             41 CALL_FUNCTION            2
             44 LOAD_CONST               5 ('Y')
             47 COMPARE_OP               2 (==)
             50 POP_JUMP_IF_FALSE      147
```

This piece of code is the equivalent of something more or less like this:

```
    from os import getenv
    if getenv('NO_CON_NAME') == 'Y':
        # rest of the code...
```

Meaning we need to set the environment variable "NO_CON_NAME" to the value "Y" to get the script to work.

```
$ NO_CON_NAME=Y python
Python 2.7.3 (default, Mar 13 2014, 11:03:55)
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import ctf_decoded
NCN6ceeeff26e72a40b71e6029a7149ad0626fcf310
```

And we finally get the right flag. :)

An alternate (shorter?) way to solve it without disassembling the Python bytecode is to just look at it in hex and try to figure out what it does:

```
>>> bytecode = """
... YwAAAAAAAAAAAwAAAEAAAABzlwAAAGQAAGQBAGwAAG0BAFoBAAFkAABkAgBsAgBtAwBaAwABZQMA
... ZAMAZAQAgwIAZAUAawIAcpMAZAYAYQQAdAQAZAcAN2EEAHQEAGQIADdhBAB0BABkCQA3YQQAdAQA
... agUAZAoAZAQAgwIAYQQAdAQAagYAZAsAgwEAYQQAZAwAZQEAdAQAgwEAagcAgwAAF2EEAG4AAGQN
... AFMoDgAAAGn/////KAEAAABzBAAAAHNoYTEoAQAAAHMGAAAAZ2V0ZW52cwsAAABOT19DT05fTkFN
... RXMAAAAAcwEAAABZczEAAAAgNTcgNjggNjEgNzQgMjAgNjkgNzMgMjAgNzQgNjggNjUgMjAgNjEg
... NjkgNzIgMmQgczEAAAAgNzMgNzAgNjUgNjUgNjQgMjAgNzYgNjUgNmMgNmYgNjMgNjkgNzQgNzkg
... MjAgNmYgczEAAAAgNjYgMjAgNjEgNmUgMjAgNzUgNmUgNmMgNjEgNjQgNjUgNmUgMjAgNzMgNzcg
... NjEgcxAAAAAgNmMgNmMgNmYgNzcgM2YgcwEAAAAgcwMAAABoZXhzAwAAAE5DTk4oCAAAAHMHAAAA
... aGFzaGxpYnMEAAAAc2hhMXMCAAAAb3NzBgAAAGdldGVudnMEAAAAZmxhZ3MHAAAAcmVwbGFjZXMG
... AAAAZGVjb2RlcwkAAABoZXhkaWdlc3QoAAAAACgAAAAAKAAAAABzCAAAADxzdHJpbmc+cwgAAAA8
... bW9kdWxlPgIAAABzEgAAABABEAEVAgYBCgEKAQoBEgEPAQ==
... """
>>> print repr(bytecode.decode("base64"))
'c\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00@\x00\x00\x00s\x97\x00\x00\x00d\x00\x00d\x01\x00l\x00\x00m\x01\x00Z\x01\x00\x01d\x00\x00d\x02\x00l\x02\x00m\x03\x00Z\x03\x00\x01e\x03\x00d\x03\x00d\x04\x00\x83\x02\x00d\x05\x00k\x02\x00r\x93\x00d\x06\x00a\x04\x00t\x04\x00d\x07\x007a\x04\x00t\x04\x00d\x08\x007a\x04\x00t\x04\x00d\t\x007a\x04\x00t\x04\x00j\x05\x00d\n\x00d\x04\x00\x83\x02\x00a\x04\x00t\x04\x00j\x06\x00d\x0b\x00\x83\x01\x00a\x04\x00d\x0c\x00e\x01\x00t\x04\x00\x83\x01\x00j\x07\x00\x83\x00\x00\x17a\x04\x00n\x00\x00d\r\x00S(\x0e\x00\x00\x00i\xff\xff\xff\xff(\x01\x00\x00\x00s\x04\x00\x00\x00sha1(\x01\x00\x00\x00s\x06\x00\x00\x00getenvs\x0b\x00\x00\x00NO_CON_NAMEs\x00\x00\x00\x00s\x01\x00\x00\x00Ys1\x00\x00\x00 57 68 61 74 20 69 73 20 74 68 65 20 61 69 72 2d s1\x00\x00\x00 73 70 65 65 64 20 76 65 6c 6f 63 69 74 79 20 6f s1\x00\x00\x00 66 20 61 6e 20 75 6e 6c 61 64 65 6e 20 73 77 61 s\x10\x00\x00\x00 6c 6c 6f 77 3f s\x01\x00\x00\x00 s\x03\x00\x00\x00hexs\x03\x00\x00\x00NCNN(\x08\x00\x00\x00s\x07\x00\x00\x00hashlibs\x04\x00\x00\x00sha1s\x02\x00\x00\x00oss\x06\x00\x00\x00getenvs\x04\x00\x00\x00flags\x07\x00\x00\x00replaces\x06\x00\x00\x00decodes\t\x00\x00\x00hexdigest(\x00\x00\x00\x00(\x00\x00\x00\x00(\x00\x00\x00\x00s\x08\x00\x00\x00<string>s\x08\x00\x00\x00<module>\x02\x00\x00\x00s\x12\x00\x00\x00\x10\x01\x10\x01\x15\x02\x06\x01\n\x01\n\x01\n\x01\x12\x01\x0f\x01'
```

We can clearly see the strings "getenv", "NCN" and "NO_CON_NAME", but "Y" is tougher to find. However, we can see other interesting strings like "hex", "sha1" and "hexdigest", and something else that looks a lot like a hex dump:

```
    57 68 61 74 20 69 73 20 74 68 65 20 61 69 72 2d
    73 70 65 65 64 20 76 65 6c 6f 63 69 74 79 20 6f
    66 20 61 6e 20 75 6e 6c 61 64 65 6e 20 73 77 61
    6c 6c 6f 77 3f
```

If we decode the hex dump we get this ASCII string:

```
    What is the air-speed velocity of an unladen swallow?
```

So it's not hard to guess we need to calculate the flag, since we know other flags in the quals look like "NCN"+hash(something), so we try this:

```
>>> import hashlib
>>> "NCN"+hashlib.sha1('What is the air-speed velocity of an unladen swallow?').hexdigest()
'NCN6ceeeff26e72a40b71e6029a7149ad0626fcf310'
```

## Other write-ups and resources

* <http://ctfcrew.org/writeup/65>)
* <http://v0ids3curity.blogspot.in/2014/09/no-con-name-ctf-quals-2014-immiscible.html>
