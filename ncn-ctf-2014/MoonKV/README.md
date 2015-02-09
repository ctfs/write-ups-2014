# NoConName 2014 Finals: MoonKV

**Category:** Misc
**Points:** ???
**Description:**

Can you see the flag?

## Write-up

We are given a .mkv video, upon examination there is an alternate audio track. Extracting this track reveals a digitally encoded image using SSTV. Using any SSTV decoding software reveals a picture of the moon landing, at the bottom of the image is the flag in red letters.

Caveat: the audio track is about 10 seconds longer than the video, so if the video processing software you're using is bad, it may get truncated. Since the flag is written at the bottom of the image, truncating the last seconds effectively removes the flag.
