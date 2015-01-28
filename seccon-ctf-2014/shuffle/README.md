# SECCON CTF 2014: Shuffle

**Category:** Binary
**Points:** 100
**Description:**

> Find the string before randomizing.
>
> [`shuffle`](shuffle)

## Write-up

```bash
$ file shuffle
shuffle: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x392b3d943f673207d169fb2c65dc642bdd79679f, not stripped

$ gdb shuffle

(gdb) disas main
Dump of assembler code for function main:
   0x0804852d <+0>: push   ebp
   0x0804852e <+1>: mov    ebp,esp
   0x08048530 <+3>: push   esi
   0x08048531 <+4>: push   ebx
   0x08048532 <+5>: and    esp,0xfffffff0
   0x08048535 <+8>: sub    esp,0x50
   0x08048538 <+11>:  mov    eax,DWORD PTR [ebp+0xc]
   0x0804853b <+14>:  mov    DWORD PTR [esp+0xc],eax
   0x0804853f <+18>:  mov    eax,gs:0x14
   0x08048545 <+24>:  mov    DWORD PTR [esp+0x4c],eax
   0x08048549 <+28>:  xor    eax,eax
   0x0804854b <+30>:  mov    eax,0x53
   0x08048550 <+35>:  mov    BYTE PTR [esp+0x24],al
   0x08048554 <+39>:  mov    eax,0x45
   0x08048559 <+44>:  mov    BYTE PTR [esp+0x25],al
   0x0804855d <+48>:  mov    eax,0x43
   0x08048562 <+53>:  mov    BYTE PTR [esp+0x26],al
   0x08048566 <+57>:  mov    eax,0x43
   0x0804856b <+62>:  mov    BYTE PTR [esp+0x27],al
   0x0804856f <+66>:  mov    eax,0x4f
   0x08048574 <+71>:  mov    BYTE PTR [esp+0x28],al
   0x08048578 <+75>:  mov    eax,0x4e
   0x0804857d <+80>:  mov    BYTE PTR [esp+0x29],al
   0x08048581 <+84>:  mov    eax,0x7b
   0x08048586 <+89>:  mov    BYTE PTR [esp+0x2a],al
   0x0804858a <+93>:  mov    eax,0x57
   0x0804858f <+98>:  mov    BYTE PTR [esp+0x2b],al
   0x08048593 <+102>: mov    eax,0x65
   0x08048598 <+107>: mov    BYTE PTR [esp+0x2c],al
   0x0804859c <+111>: mov    eax,0x6c
   0x080485a1 <+116>: mov    BYTE PTR [esp+0x2d],al
   0x080485a5 <+120>: mov    eax,0x63
   0x080485aa <+125>: mov    BYTE PTR [esp+0x2e],al
   0x080485ae <+129>: mov    eax,0x6f
   0x080485b3 <+134>: mov    BYTE PTR [esp+0x2f],al
   0x080485b7 <+138>: mov    eax,0x6d
   0x080485bc <+143>: mov    BYTE PTR [esp+0x30],al
   0x080485c0 <+147>: mov    eax,0x65
   0x080485c5 <+152>: mov    BYTE PTR [esp+0x31],al
   0x080485c9 <+156>: mov    eax,0x20
   0x080485ce <+161>: mov    BYTE PTR [esp+0x32],al
   0x080485d2 <+165>: mov    eax,0x74
   0x080485d7 <+170>: mov    BYTE PTR [esp+0x33],al
   0x080485db <+174>: mov    eax,0x6f
   0x080485e0 <+179>: mov    BYTE PTR [esp+0x34],al
   0x080485e4 <+183>: mov    eax,0x20
   0x080485e9 <+188>: mov    BYTE PTR [esp+0x35],al
   0x080485ed <+192>: mov    eax,0x74
   0x080485f2 <+197>: mov    BYTE PTR [esp+0x36],al
   0x080485f6 <+201>: mov    eax,0x68
   0x080485fb <+206>: mov    BYTE PTR [esp+0x37],al
   0x080485ff <+210>: mov    eax,0x65
   0x08048604 <+215>: mov    BYTE PTR [esp+0x38],al
   0x08048608 <+219>: mov    eax,0x20
   0x0804860d <+224>: mov    BYTE PTR [esp+0x39],al
   0x08048611 <+228>: mov    eax,0x53
   0x08048616 <+233>: mov    BYTE PTR [esp+0x3a],al
   0x0804861a <+237>: mov    eax,0x45
   0x0804861f <+242>: mov    BYTE PTR [esp+0x3b],al
   0x08048623 <+246>: mov    eax,0x43
   0x08048628 <+251>: mov    BYTE PTR [esp+0x3c],al
   0x0804862c <+255>: mov    eax,0x43
   0x08048631 <+260>: mov    BYTE PTR [esp+0x3d],al
   0x08048635 <+264>: mov    eax,0x4f
   0x0804863a <+269>: mov    BYTE PTR [esp+0x3e],al
   0x0804863e <+273>: mov    eax,0x4e
   0x08048643 <+278>: mov    BYTE PTR [esp+0x3f],al
   0x08048647 <+282>: mov    eax,0x20
   0x0804864c <+287>: mov    BYTE PTR [esp+0x40],al
   0x08048650 <+291>: mov    eax,0x32
   0x08048655 <+296>: mov    BYTE PTR [esp+0x41],al
   0x08048659 <+300>: mov    eax,0x30
   0x0804865e <+305>: mov    BYTE PTR [esp+0x42],al
   0x08048662 <+309>: mov    eax,0x31
   0x08048667 <+314>: mov    BYTE PTR [esp+0x43],al
   0x0804866b <+318>: mov    eax,0x34
   0x08048670 <+323>: mov    BYTE PTR [esp+0x44],al
   0x08048674 <+327>: mov    eax,0x20
   0x08048679 <+332>: mov    BYTE PTR [esp+0x45],al
   0x0804867d <+336>: mov    eax,0x43
   0x08048682 <+341>: mov    BYTE PTR [esp+0x46],al
   0x08048686 <+345>: mov    eax,0x54
   0x0804868b <+350>: mov    BYTE PTR [esp+0x47],al
   0x0804868f <+354>: mov    eax,0x46
   0x08048694 <+359>: mov    BYTE PTR [esp+0x48],al
   0x08048698 <+363>: mov    eax,0x21
   0x0804869d <+368>: mov    BYTE PTR [esp+0x49],al
   0x080486a1 <+372>: mov    eax,0x7d
   0x080486a6 <+377>: mov    BYTE PTR [esp+0x4a],al
   0x080486aa <+381>: mov    eax,0x0
   0x080486af <+386>: mov    BYTE PTR [esp+0x4b],al
   0x080486b3 <+390>: mov    DWORD PTR [esp],0x0
   0x080486ba <+397>: call   0x80483b0 <time@plt>
   0x080486bf <+402>: mov    ebx,eax
   0x080486c1 <+404>: call   0x80483d0 <getpid@plt>
   0x080486c6 <+409>: add    eax,ebx
   0x080486c8 <+411>: mov    DWORD PTR [esp],eax
   0x080486cb <+414>: call   0x8048400 <srand@plt>
   0x080486d0 <+419>: mov    DWORD PTR [esp+0x14],0x0
   0x080486d8 <+427>: jmp    0x8048769 <main+572>
   0x080486dd <+432>: call   0x8048420 <rand@plt>
   0x080486e2 <+437>: mov    ecx,eax
   0x080486e4 <+439>: mov    edx,0xcccccccd
   0x080486e9 <+444>: mov    eax,ecx
   0x080486eb <+446>: mul    edx
   0x080486ed <+448>: shr    edx,0x5
   0x080486f0 <+451>: mov    eax,edx
   0x080486f2 <+453>: shl    eax,0x2
   0x080486f5 <+456>: add    eax,edx
   0x080486f7 <+458>: shl    eax,0x3
   0x080486fa <+461>: sub    ecx,eax
   0x080486fc <+463>: mov    edx,ecx
   0x080486fe <+465>: mov    DWORD PTR [esp+0x18],edx
   0x08048702 <+469>: call   0x8048420 <rand@plt>
   0x08048707 <+474>: mov    ecx,eax
   0x08048709 <+476>: mov    edx,0xcccccccd
   0x0804870e <+481>: mov    eax,ecx
   0x08048710 <+483>: mul    edx
   0x08048712 <+485>: shr    edx,0x5
   0x08048715 <+488>: mov    eax,edx
   0x08048717 <+490>: shl    eax,0x2
   0x0804871a <+493>: add    eax,edx
   0x0804871c <+495>: shl    eax,0x3
   0x0804871f <+498>: sub    ecx,eax
   0x08048721 <+500>: mov    edx,ecx
   0x08048723 <+502>: mov    DWORD PTR [esp+0x1c],edx
   0x08048727 <+506>: lea    edx,[esp+0x24]
   0x0804872b <+510>: mov    eax,DWORD PTR [esp+0x18]
   0x0804872f <+514>: add    eax,edx
   0x08048731 <+516>: movzx  eax,BYTE PTR [eax]
   0x08048734 <+519>: movsx  eax,al
   0x08048737 <+522>: mov    DWORD PTR [esp+0x20],eax
   0x0804873b <+526>: lea    edx,[esp+0x24]
   0x0804873f <+530>: mov    eax,DWORD PTR [esp+0x1c]
   0x08048743 <+534>: add    eax,edx
   0x08048745 <+536>: movzx  eax,BYTE PTR [eax]
   0x08048748 <+539>: lea    ecx,[esp+0x24]
   0x0804874c <+543>: mov    edx,DWORD PTR [esp+0x18]
   0x08048750 <+547>: add    edx,ecx
   0x08048752 <+549>: mov    BYTE PTR [edx],al
   0x08048754 <+551>: mov    eax,DWORD PTR [esp+0x20]
   0x08048758 <+555>: lea    ecx,[esp+0x24]
   0x0804875c <+559>: mov    edx,DWORD PTR [esp+0x1c]
   0x08048760 <+563>: add    edx,ecx
   0x08048762 <+565>: mov    BYTE PTR [edx],al
   0x08048764 <+567>: add    DWORD PTR [esp+0x14],0x1
   0x08048769 <+572>: cmp    DWORD PTR [esp+0x14],0x63
   0x0804876e <+577>: jle    0x80486dd <main+432>
   0x08048774 <+583>: lea    eax,[esp+0x24]
   0x08048778 <+587>: mov    DWORD PTR [esp],eax
   0x0804877b <+590>: call   0x80483e0 <puts@plt>
   0x08048780 <+595>: mov    eax,0x0
   0x08048785 <+600>: mov    esi,DWORD PTR [esp+0x4c]
   0x08048789 <+604>: xor    esi,DWORD PTR gs:0x14
   0x08048790 <+611>: je     0x8048797 <main+618>
   0x08048792 <+613>: call   0x80483c0 <__stack_chk_fail@plt>
   0x08048797 <+618>: lea    esp,[ebp-0x8]
   0x0804879a <+621>: pop    ebx
   0x0804879b <+622>: pop    esi
   0x0804879c <+623>: pop    ebp
   0x0804879d <+624>: ret
End of assembler dump.
(gdb)
```

The `main` function contains a lot of hardcoded numeric values, the first of which can be seen at `0x0804854b` and the last of which is a `0x0` at `0x080486aa`. Here’s the full list:

```
0x53
0x45
0x43
0x43
0x4f
0x4e
0x7b
0x57
0x65
0x6c
0x63
0x6f
0x6d
0x65
0x20
0x74
0x6f
0x20
0x74
0x68
0x65
0x20
0x53
0x45
0x43
0x43
0x4f
0x4e
0x20
0x32
0x30
0x31
0x34
0x20
0x43
0x54
0x46
0x21
0x7d
0x0
```

Those all look like Unicode code points in the ASCII range. Let’s turn these numbers into a string:

```bash
$ node
> String.fromCharCode(0x53, 0x45, 0x43, 0x43, 0x4f, 0x4e, 0x7b, 0x57, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 0x65, 0x20, 0x74, 0x6f, 0x20, 0x74, 0x68, 0x65, 0x20, 0x53, 0x45, 0x43, 0x43, 0x4f, 0x4e, 0x20, 0x32, 0x30, 0x31, 0x34, 0x20, 0x43, 0x54, 0x46, 0x21, 0x7d, 0x0)
'SECCON{Welcome to the SECCON 2014 CTF!}\0'
```

It’s indeed a null-terminated string that contains the flag `SECCON{Welcome to the SECCON 2014 CTF!}`.

## Other write-ups and resources

* [Portuguese](https://ctf-br.org/wiki/seccon/seccon2014/r100-shuffle/)
