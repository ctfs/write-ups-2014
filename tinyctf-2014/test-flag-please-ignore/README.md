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

## Other write-ups

* none yet
