# Plaid CTF 2014: bronies

**Category:** Web
**Points:** 500
**Description:**

> We are trying to break into eXtreme Secure Solutions, where The Plague works as a system adminstrator. We have found that their internal company login page is at <http://portal.essolutions.largestctf.com/>. Recon has also revealed that The Plague likes to browse this site during work hours: <http://54.196.225.30/> using the username `ponyboy2004`.
> Remember, our main target is to break into the company portal, *not* the pony site.
>
> UPDATE: The SQL injection was not intentional and does not help you solve the problem. We believe it has been fixed. If you have questions, please ask ricky on #pctf @ sendak.freenode.net.
> UPDATE2: Also, bronies is not intended to be solved via client side (e.g. WebKit) exploits - if you manage to do so though, that's fair game.
> UPDATE3: Bronies was broken until 2013-04-13 07:26:28 UTC (the admin wasn't logging onto the internal portal properly). Please retry your exploits.
> UPDATE4: Sorry, once again, please retry your bronies part 1 exploits. We think we fixed a bug at 2013-04-13 08:33:30 UTC that was breaking some attempts.
>
> Hint: just to clarify, both flags for bronies are behind the login page - the pony site doesn't have any flags in it.

## Write-up

(TODO)

The first flag is `xss_problem_is_web_problem`. The second flag is `WEB_you_hacked_the_bigson_WEB`.

## Other write-ups and resources

* <https://fail0verflow.com/blog/2014/plaidctf2014-web800-bronies.html>
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/bronies)
