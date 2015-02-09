# HITCON CTF 2014: Pneumotoulthamicrescopicfilicoloaganiconissis

**Category:** Trivia
**Points:** 80
**Description:**

> [https://raw.githubusercontent.com/hitcon2014ctf/ctf/master/Pneumotoulthamicrescopicfilicoloaganiconissis-df5bb3d8f83d6d37e16560062cb231bc.txt](Pneumotoulthamicrescopicfilicoloaganiconissis-df5bb3d8f83d6d37e16560062cb231bc.txt)
> [https://dl.dropbox.com/s/c90ozt18mxmriko/Pneumotoulthamicrescopicfilicoloaganiconissis-df5bb3d8f83d6d37e16560062cb231bc.txt](Pneumotoulthamicrescopicfilicoloaganiconissis-df5bb3d8f83d6d37e16560062cb231bc.txt)

**Hint:**

> diff the file content and the origin english word (try to find it out)

## Write-up

By searching for the string (just part of it) in the google we find out that it's the [http://en.wikipedia.org/wiki/Longest_word_in_English](longest word) that contains 189 819 characters and apparenty (by reading the hint) it was modified. We need to obtain the original one. Some more Googling reveals the word in its full form: <http://www.digitalspy.co.uk/fun/news/a444700/longest-word-has-189819-letters-takes-three-hours-to-pronounce.html>.

Now that we have the original, we can write a short Python script:

```python
longest = '' # put the longest word here
longest_modified = '' # put the modified longest word here
i = 0
password = ''
plLen = len(longest_modified)

for j in range(0, plLen):
  c = longest_modified[j]
  d = longest[i]
  if c != d:
    password = password + c
  i = i + 1
  j = j + 1

print password
```

Running the script produces:

```
HITCON{This flag is longestestestestestestestestestestestestestestestestestestestestestestestestestest!!!}
```

…which is the flag.

## Other write-ups and resources

* <https://ucs.fbi.h-da.de/writeup-hitcon-pneumo/>
* <https://rzhou.org/~ricky/hitcon2014/pneumotoulthamicrescopicfilicoloaganiconissis/>
