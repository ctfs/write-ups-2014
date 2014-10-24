# Hack.lu CTF 2014: Get your gatling at Garrettling! (Part 2)

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
> Task B: Oh, my sweet revenge.
>
> Let’s talk about revenge. I know our sheriff would not support it, but hey, Mr Garret was one of my closest friends and I demand revenge! To add a bit of symbolism — after all, we’re in a Western — I want to pay the f*cker back using the very same weapon.
>
> Unfortunately, every Behemot is tied to a certain processing unit. In absence of the corresponding unit, the weapon won’t fire at all. We do not have said unit. Can you make the weapon fire regardless?
>
> [The flag corresponds to the trait the weapon expects from the correct processing unit and starts with `FLG_` (+ASCII) and is 32 bytes in size in total.]
>
> (*): Given you start to shoot about 30 seconds early.
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
