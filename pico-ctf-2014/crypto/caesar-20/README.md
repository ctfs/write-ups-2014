# Pico CTF 2014 : Caesar

**Category:** Crypto
**Points:** 20
**Description:**

>You find an encrypted message written on the documents. Can you decrypt it?

**Hint:**
>Is there a cipher named the same as the title of this problem?

## Write-up

We rotate the text using the caesar cipher using [this tool]():

```bash
$ for i in {0..25}; do python rot.py -l $i espdpncpealddascldptdfvaaychcjplgrehtnqxycvmykpblhr; done
espdpncpealddascldptdfvaaychcjplgrehtnqxycvmykpblhr
ftqeqodqfbmeebtdmequegwbbzdidkqmhsfiuoryzdwnzlqcmis
[...]
sgdrdbqdsozrrogqzrdhrtjoomqvqxdzufsvhbelmqjamydpzvf
thesecretpassphraseisukppnrwryeavgtwicfmnrkbnzeqawg
uiftfdsfuqbttqisbtfjtvlqqosxszfbwhuxjdgnoslcoafrbxh
[...]
```

The flag is `ukppnrwryeavgtwicfmnrkbnzeqawg`.

## Other write-ups and resources

* <http://ehsandev.com/pico2014/cryptography/caesar.html>
* <https://ctf-team.vulnhub.com/picoctf-2014-ceasar/>
