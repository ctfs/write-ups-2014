# Hack.lu CTF 2014: Get your gatling at Garrettling! (Part 1)

**Category:** Reversing
**Points:** 500
**Author:** dwuid
**Description:**

> That’s how we promote… well, used to promote our fine, handcrafted gatlings. Proven quality, make you survive every duel (*).
>
> The business flourished, up to the point where someone decided to murder our eponymous company owner, Pat Garrett. Too sad, since we just started delivering our newest product, the Behemot gatling.
>
> Cruel as this world seems to be, apparently, Mr Garrett has been killed by the very same weapon! It must have been one of our loyal customers. At least one of the hundred customers that bought a Behemot. Anyway, we could at least get hold of the weapon. Not of the murderer, though.
>
> [Download](garretling_92f4f4f9492d261a20bf7b7450c7c7a3.exe)
>
> Task A: Be Sherlock, my friend.
>
> Since we cannot afford having all customers killed, we must ask you to help us find the murderer. Clever as he is, Mr Garrett fabricated every Behemot slightly different. The differences help us find the customer who once bought the murder weapon.
>
> Mr Garrett kept notes on the way he designed the Behemots. Maybe you can decipher them and tell us who bought the weapon?
>
> [The flag corresponds to the embedded fingerprint value and starts with `FLG_` (+ASCII).]
>
> (*): Given you start to shoot about 30 seconds early.
>
> Technical Notes on the fingerprinting scheme:
> - The fingerprint value is hidden within the protection code (based on Virtual Machines).
> - In order to extract the mark, you will need to:
>   * group equivalent handlers in order to
>   * assign bits to them.
> - Every handler corresponds to an opcode value (the index of said handler in the handler table).
> - Bits are assigned to each handler that encode a part of the fingerprint value.
> - Ex.: If there are four handlers implementing the same semantics (“equivalent” handlers), each virtual instruction encodes `log_2(4)` = `2` bits depending on the handler it is encoded with.
>
> The two bit values are assigned in ascending order, starting with the _lowest_ opcode:
>
> ```opcode handler semantics assigned bits
> 04 vm_exit 00
> 97 vm_exit 01
> b3 vm_exit 10
> d0 vm_exit 11
> ```
>
> `vm_exit` can be encoded using opcode `04`, `97`, `b3` or `d0`.
> If the virtual instruction `vm_exit` is in one instance encoded as `0xb3`, it encodes two bits of the fingerprint value, namely: `10_2`.
> - All virtual instructions hence encode parts of the fingerprint value. It might be the case that for certain instructions, only one single handler implements the necessary semantics. Intuitively, these instructions cannot encode any bit, as `log_2(1) = 0`.
> - The value/flag is encoded in the first few virtual instructions/opcodes (at `0x4d9414`) and is 256 bits long.
> - Keep in mind that opcodes are encrypted and decryption keys are reset on branches! You will need to emulate opcode decryption.
>
> Flag has a length of 48 bytes.
>
> #### Update
>
> The challenge text gave a different VA for the beginning of the bytecode, actually, it’s `0x4d945d`.
>
> There are 37 unique VM handlers — which does not mean all of them are actually used. Others are duplicates, match characteristics to find them.
>
> Obfuscation for Garrettling’s VM is pattern-based. Remove it by searching for patterns listed below and simplifying them repeatedly.
>
> Only some instructions are obfuscated, iteratively:
>
> ```
> * push arg:
> -------------------------------------------------------
> call _off_1_to_7
> db junk_bytes ; ...
>
> _off_1_to_7:
> mov dword ptr [esp], arg
>
> * push arg:
> -------------------------------------------------------
> push imm ; or: push random_reg
> mov size ptr [esp], arg
>
> * push arg:
> -------------------------------------------------------
> lea esp, dword ptr [esp - 4]
> mov size ptr [esp], arg
>
> * pop arg:
> -------------------------------------------------------
> lea esp, dword ptr [esp + 4]
> mov arg, size ptr [esp - 4]
>
> * cmp dst, src:
> -------------------------------------------------------
> push dst
> add dst, -src_imm
> pop dst
>
> * cmp dst, src:
> -------------------------------------------------------
> push dst
> not src
> add dst, src
> not src
> pop dst
>
> * add dst, src
> -------------------------------------------------------
> sub dst, -src_imm
>
> * add dst, src
> -------------------------------------------------------
> lea dst, dword ptr [dst + src_imm]
>
> * pushf:
> -------------------------------------------------------
> push eax
> lahf
> and eax, 0xff00
> shr eax, 8
> push eax
> push dword ptr [esp + 4]
> pop eax
> pop dword ptr [esp]
>
> * popf:
> -------------------------------------------------------
> push eax
> mov eax, dword ptr [esp + 4]
> shl eax, 8
> sahf
> pop eax
> lea esp, dword ptr [esp + 4]
>
> * mov dst, src:
> -------------------------------------------------------
> push src
> pop dst
>
> * xor dst, src:
> -------------------------------------------------------
> push dst
> not dst
> and dst, src_imm
> push dst
> mov dst, size ptr [esp + size]
> and dst, (~src_imm)
> or dst, size ptr [esp]
> lea esp, dword ptr [esp + 8]
>
> * xor dst, src:
> -------------------------------------------------------
> push src
> push dst
> not dst
> push src
> and dst, src
> pop src
> not src
> and src, size ptr [esp]
> lea esp, dword ptr [esp + size]
> or dst, src
> pop src
> ```

## Write-up

(TODO)

## Other write-ups and resources

* none yet
