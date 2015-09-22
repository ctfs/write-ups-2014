# Ghost in the Shellcode 2014: Ad Subtract

**Category:** Choose your Pwn Adventure 2
**Points:** 75
**Description:**

> Challenge available from within PwnAdventure2.

## Write-up

The challenge (as explained by an in-game NPC) was to get rid of the ad diplayed in the Game Menu.

Traffic sniffing showed that after starting the game, a request was made to the domain `dontpanicsoftware.com` which delivered the ad images. Let’s route such requests to `localhost`, so we can serve a transparent PNG image instead:

```bash
$ echo '127.0.0.1 dontpanicsoftware.com # GitS2014: Ad Subtract' | sudo tee -a /etc/hosts

$ dscacheutil -flushcache && killall -HUP mDNSResponder
```

After restarting the game, the ads are now transparent/invisible. This reveals the underlying text: `AdBlockedHaveASillyMooseAnyway`.

## Other write-ups and resources

* <http://tasteless.eu/2014/01/gits-2014-ad-substract-pwn-adventure-75>
