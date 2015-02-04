# DEFKTHON CTF: Web 200

**Description:**

> [Auth Me In](http://54.201.96.212:888/web200/)

## Write-up

The hint [“Not SQL”](https://twitter.com/OpenSecurity_IN/status/440536455614443521) tells us not to look for SQL injection. After searching on the Internet about injections that are not an SQL injection, I came up with something called [a NoSQL injection](http://data.story.lu/2011/03/07/nosql-injection-in-mongo-php). A quick look at it and you will learn that, by appending `[$ne]` to the `$_GET` parameter, you can, instead make the query look for things that are ‘not equal’ to whatever you set the value to.

The final solution that resulted in the flag `flag{itoldunaathisisnotSQLinjection}` was `http://54.201.96.212:888/web200/?userid[$ne]=a&password[$ne]=a`.

## Other write-ups and resources

* <http://tasteless.eu/2014/03/defkthon-ctf-2014-web200-web300-and-web400-writeup/>
* [Japanese](http://hority-ctf.blogspot.jp/2014/03/defkthon-ctf-2014-write-up.html)
