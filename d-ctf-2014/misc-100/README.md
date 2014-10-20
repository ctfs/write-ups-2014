# D-CTF 2014: Misc 100 – SE FTW

**Category:** Misc
**Points:** 100
**Description:**

> In two words describe social engineering!
>
> **Hint:** 2f722f6e6574736563

## Write-up

Since the hint consists of hexadecimal digits only, let’s try to decode it:

```bash
$ xxd -r -p <<< 2f722f6e6574736563
/r/netsec
```

[/r/netsec](https://www.reddit.com/r/netsec) is a subreddit where information security news is discussed. In its sidebar contains a bunch of links, including this one:

> /r/SocialEngineering - Free Candy

The flag is `free candy`.

## Other write-ups and resources

* none yet
