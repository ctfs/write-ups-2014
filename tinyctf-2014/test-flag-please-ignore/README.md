# tinyCTF 2014: Test flag, please ignore

**Category:** Misc
**Points:** 10
**Description:**

> [Download file](misc10.zip)

## Write-up

Extracting the provided `misc10.zip` file reveals a text file with the following contents:

```
666c61677b68656c6c6f5f776f726c647d
```

Since this wasn’t accepted as the solution (and neither was `flag{666c61677b68656c6c6f5f776f726c647d}`), I tried to hex-decode it:

```bash
$ xxd -r -p <<< 666c61677b68656c6c6f5f776f726c647d
flag{hello_world}
```

The flag is `flag{hello_world}`.

## Other write-ups and resources

* <http://sugarstack.io/tinyctf-misc-10.html>
* <https://poerhiza.github.io/ctf/2014/10/05/tinyCTF-write_ups-test_flag_please_ignore/>
* <https://github.com/jesstess/tinyctf/blob/master/test/test.md>
