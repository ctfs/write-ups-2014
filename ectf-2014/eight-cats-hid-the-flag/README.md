# ECTF 2014: Eight Cats Hid the Flag

**Category:** Recon
**Points:** 100
**Description:**

> Find the flag.
>
> **Hint:** Have you learnt a version control system before? Because one of our team members says he has.

## Write-up

“Eight cats” is a hint at [Octocat, the official GitHub mascot](https://octodex.github.com/). We probably have to look for the flag on one of the CTF organizer’s GitHub repositories.

Cloning all of @karthiksenthil’s repositories and `grep`ping for a flag yields no results. There seems to be no other way of finding the flag except manually going through all commits, as the flag has been deleted from the source code. The commit in question was made a month before the CTF started, which made things a bit more difficult. By manually looking through all the commits we eventually found commit https://github.com/karthiksenthil/Learn-Git/commit/9cd4ecad6f7c545ef5ac31622d503de811191d7b which contains the flag `flag{0ctocat_c4n_play_h1de_and_s33k}`.

## Other write-ups and resources

* <http://dhanvi1.wordpress.com/2014/10/23/eight-cats-hid-the-flag-ectf-2014-recon-100-writeup/>
