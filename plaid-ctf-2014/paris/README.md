# Plaid CTF 2014: paris

**Category:** Reversing
**Points:** 300
**Description:**

> [This binary](paris-20b542bf824d8d0daf240bbf3febbce0.tar.bz2) was found on some of our Windows machines. It's got The Plague written all over it. What secrets are contained inside?

## Write-up

The binary is a password crackme. It uses a VM with 20 different opcodes for obfuscating the password checking algorithm. The VM does some peculiar things however.

We need to find a password such that ESI has the value `0xdeadbeef` after `process_password` gets called:

```nasm
.text:00401056 call    process_password
.text:0040105B push    0FFFFFFF5h                      ; nStdHandle
.text:0040105D call    ds:GetStdHandle
.text:00401063 push    0
.text:00401065 push    offset NumberOfCharsWritten
.text:0040106A cmp     esi, 0DEADBEEFh
.text:00401070 jnz     try_again
```

Looking at `process_password` each attempt to decode a VM instruction also generates an exception:

```nasm
.text:00402066 process_password proc near
.text:00402066 xor     ecx, ecx
.text:00402068
.text:00402068 loop_vm:
.text:00402068 push    offset seh_handler
.text:0040206D push    large dword ptr fs:0
.text:00402074 mov     large fs:0, esp
.text:0040207B mov     eax, 0
.text:00402080 mov     [eax], eax                      ; jump to seh_handler
.text:00402082 sub     edi, 1111h                      ; also important
.text:00402088 pop     large dword ptr fs:0
.text:0040208F add     esp, 4
.text:00402092 cmp     vm_done_flag, 1
.text:00402099 jz      vm_done
.text:0040209F jmp     short loop_vm
.text:0040209F process_password endp
```

It seems the SEH handler is actually responsible for decoding the instructions. Also, note the `sub edi, 1111h` which will be important later.

Looking at the SEH handler:

```nasm
.text:00402376 seh_handler:
.text:00402376 movzx   eax, byte ptr vm_current_opcode_dispatch
.text:0040237D add     eax, offset vm_opcode_dispatch
.text:00402382 mov     eax, [eax]
.text:00402384 add     byte ptr vm_current_opcode_dispatch, 4
.text:0040238B cmp     byte ptr vm_current_opcode_dispatch, 50h
.text:00402392 jl      short loc_40239B
.text:00402394 mov     byte ptr vm_current_opcode_dispatch, 0
.text:0040239B
.text:0040239B loc_40239B:
.text:0040239B jmp     eax
```

It doesn’t seem to do anything too special. It just loops through an array of functions for each exception that gets generated.

Looking at the function array:

```nasm
.text:0040220E vm_opcode_dispatch dd offset vm_0_nop
.text:00402212 dd offset vm_201_mov_r_r
.text:00402216 dd offset vm_202_mov_r_r
.text:0040221A dd offset vm_203_mov_r_mem_r_
.text:0040221E dd offset vm_13_mov_r_imm16
.text:00402222 dd offset vm_98_add_r_r
.text:00402226 dd offset vm_99_sub_r_r
.text:0040222A dd offset vm_9a_xor_r_r
.text:0040222E dd offset vm_9b_and_r_r
.text:00402232 dd offset vm_9_shr_r_8
.text:00402236 dd offset vm_15_not_r
.text:0040223A dd offset vm_2_inc_r
.text:0040223E dd offset vm_3f_cmp_r_r
.text:00402242 dd offset vm_1f_jmp_imm
.text:00402246 dd offset vm_1d_jz_imm
.text:0040224A dd offset vm_7_push_r
.text:0040224E dd offset vm_18_pop_r
.text:00402252 dd offset vm_1b_bswap_r
.text:00402256 dd offset vm_0a_xor_decrypt      ;; "unorthodox" instruction (XORs 200h bytes)
.text:0040225A dd offset vm_14_done
```

Looking at some of the handlers, some patterns emerge. There are three helper functions used in the instruction handlers:

1. `00401CF0 vm_1byte_instruction_ebx`
2. `00401D19 vm_2byte_instruction_ebx_ecx`
3. `00401D50 vm_3byte_instruction_ebx_ecx`

Each of these functions reads in the next bytes in the code stream and returns the decode opcode in `eax` and operands in `ebx` and `ecx`.

Another peculiar thing is that each instruction handler will subtract a value (the opcode) from `eax` and `setz al` before jumping to this code:

```nasm
.text:00401FCA mov     edx, [esp+arg_8]
.text:00401FCE cmp     al, 1
.text:00401FD0 jz      inc_eh_ret_by_2
.text:00401FD6 mov     esi, offset vm_copy_of_host_cpu_registers
.text:00401FDB mov     edi, edx
.text:00401FDD mov     ecx, 34h
.text:00401FE2 rep movsd
.text:00401FE4 mov     esi, offset vm_copy_of_password_buff
.text:00401FE9 mov     edi, offset password_buff       ; "V1rTu4L_M"
.text:00401FEE mov     ecx, 100h
.text:00401FF3 rep movsd
.text:00401FF5 mov     esi, 401890h
.text:00401FFA mov     edi, offset vm_unknown_input
.text:00401FFF mov     ecx, 80h
.text:00402004 rep movsd
.text:00402006 mov     al, byte_4024AB
.text:0040200B mov     vm_zf, al
.text:00402010 mov     al, initial_vm_done_flag
.text:00402015 mov     vm_done_flag, al
.text:0040201A mov     ax, vm_ip_copy
.text:00402020 mov     vm_ip, ax
.text:00402026 mov     ax, vm_sp_copy
.text:0040202C mov     vm_sp, ax
.text:00402032 jmp     inc_eh_ret_by_2
```

That checks if `al` is `1` (i.e. if `setz al` set it to `1`). If `al` was not set to `1`, it reverts the VM to the state before executing that instruction. This is probably the weirdest thing about this VM, it checks and runs the VM code and reverts if it later figures out that it wasn’t the proper opcode for the instruction it just executed.

The VM registers seem to be kept at `[esp+0Ch]+9ch`. This is all running inside a SEH handler and `[esp+0Ch]` points to the CONTEXT struct which contains (among other things) the register state when the exception occured. At offset `9ch` in the CONTEXT struct you have the EDI register. Based on the instruction handlers and the 3 helper functions the VM seems to be all 16-bit and has 3 bits for register encoding in the instructions (that means 8 general purpose registers in total). So `r0`-`r7` (VM registers) seem to be overlayed on top of EDI, ESI, EBX, EDX. Now, remember the `sub edi, 1111h` happening for each instruction decoded? That’s going to change `r0` and `r1` inside the VM (ouch) each time an attempt to decode an opcode is made.

Note: This is the long way (my way) of doing this, you can probably put a conditional breakpoint right after the call to one of the three helper functions and check if `eax` has the proper opcode value and trace.

I wrote [a simple script](disasm.py) to disassemble all the VM code and then formatted it to something more pleasant (I tend to like static analysis better). This resulted in:

```nasm
[0000] nop
[0001] nop
[0002] nop
[0003] mov r2, 0x3133
[0006] mov r3, 0x0
[0009] mov r4, 0xff00
[000c] mov r5, 0xff
loop_mem:
  [000f] mov r0, word [r3]    ;; actually r0 = [r3] - 3332h, because of sub edi, 1111h and the loopy behavior
  [0011] mov r7, r0
  [0013] bswap r7
  [0014] not r7
  [0015] cmp r7, r2
  [0017] jz loop_mem_exit
  [001a] mov r6, r7
  [001c] and r6, r4
  ;; r7 = word[r3] & 0xff
  [001e] and r7, r5
  ;; r6 = word[r3] & 0xff00 >> 8
  [0020] shr r6, 8
  [0021] xor r7, r6
  ;; r6 = 0x200
  [0023] mov r6, 0x200
  [0026] add r7, r7
  [0028] add r6, r7
  [002a] mov r7, word [r6]
  [002c] bswap r7
  [002d] pop r6
  [002e] xor r7, r6
  [0030] push r6
  [0031] push r7
  [0032] xor200h r3
  [0033] inc r3
[0034] jmp loop_mem
loop_mem_exit:
;; r7 = 0
;; r2 = 0x100
;; r6 = 0xaf21
[0037] xor r7, r7
[0039] mov r2, 0x100
[003c] mov r6, 0xaf21
loop_stack:
  [003f] mov r5, word [r2]
  [0041] bswap r5
  [0042] inc r2
  [0043] inc r2
  [0044] pop r3    ;; need to pop 0x5a4d here before r5 == 0xaf21, stack also needs to be aligned after that pop
  [0045] cmp r5, r6
  [0047] jz good_boy
  [004a] cmp r5, r3
  [004c] jz loop_stack
[004f] mov r3, 0x0
[0052] mov r2, 0x0
[0055] done
good_boy:
[0056] mov r5, 0x5a4d
[0059] cmp r3, r5    ;; r3 needs to be 0x5a4d
[005b] jz good_boy_final
[005e] mov r3, 0x0
[0061] mov r2, 0x0
[0064] done
good_boy_final:
[0065] mov r3, 0xdead   ;; r2 and r3 overlay on top of ESI which we want to be set to 0xdeadbeef
[0068] mov r2, 0xbeef
```

The base of memory seems to be where the password read from the keyboard is stored (`00401490`). What the VM code appears to be doing is pushing some values to the stack in the first loop and in the second loop it compares the stack with the values at `MEM_100h`. Also note the use of `r0` which gets changed in each attempt to decode an instruction.

And this (in reverse) is what the stack should look like:

```nasm
.text:00401590 dw 2E0Bh
.text:00401592 dw 6D02h
.text:00401594 dw 7492h
.text:00401596 dw 870Ch
.text:00401598 dw 93B9h
.text:0040159A dw 0EDB3h
.text:0040159C dw 312Ch
.text:0040159E dw 7107h
.text:004015A0 dw 7D10h
.text:004015A2 dw 2007h
.text:004015A4 dw 0E7C6h
.text:004015A6 dw 3A1Bh
.text:004015A8 dw 0BAD8h
.text:004015AA dw 9417h
.text:004015AC dw 0FA6Bh
.text:004015AE dw 0BE6Ch
.text:004015B0 dw 621Dh
.text:004015B2 dw 4D3Bh
.text:004015B4 dw 47ADh
.text:004015B6 dw 7A7Ah
.text:004015B8 dw 3E9Dh
.text:004015BA dw 53A2h
.text:004015BC dw 0F22Fh
.text:004015BE dw 0D1A9h
.text:004015C0 dw 0F574h
.text:004015C2 dw 8173h
.text:004015C4 dw 11BCh
.text:004015C6 dw 0AE15h
.text:004015C8 dw 6179h
.text:004015CA dw 0AF21h    ;; this actually needs to be 0x5a4d which is already the top of the stack
```

So we need to find a password for which each adjacent two characters with the `sub` and `xor` will point to an index in `MEM_200h` where a uint16 is found that when XORed with the top of the stack should yield the next value from the array at `MEM_100h`. *gasp*

Note: There may be a nicer way of doing this next thing (compared to what I did) but it took me a while to figure out the importance of `sub edi, 1111h` and I was a bit paranoid that subtracting `3332h` would make the guessing more complicated due to carry between high and low bytes. I imagine you can roll `MEM_200h` to the last iteration and check the last value and unroll `MEM_200h` and check the second value and maybe that would be easier.

So, what I did was bruteforce all possible candidate pairs of “printable” characters for each word that needs to be on the stack and then combine them in sequence to get the flag. My script is named [`messy.py`](messy.py). Run it as follows:

```bash
$ python messy.py
```

Among the things my messy script produced was:

```nasm
('V', ('1', ('r', ('T', ('u', ('4', ('L', ('_', ('M', ('4', ('c', ('h', ('1', ('n', ('3', ('s', ('_', ('4', ('r', ('3',
('_', ('A', ('w', ('3', ('s', ('0', ('m', ('3', None))))))))))))))))))))))))))))
```

Well, it was missing the last `!` character, but meh. The flag was `V1rTu4L\_M4ch1n3s\_4r3\_Aw3s0m3!`.

## Other write-ups and resources

* <http://idabook.com/paris_writeup.txt> by Chris Eagle
* <https://fail0verflow.com/blog/2014/plaidctf2014-re300-paris.html>
* <http://piggybird.net/2014/04/plaidctf-2014-reversing-300-paris/>
