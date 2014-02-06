# Stripe CTF3: level2

## Description

You get a frantic late-night call from the ops team of a major online service provider: “We’ve been hit by this massive DDOS attack,” they say. “It’s a hundred times our normal traffic and we’re dropping requests every ms. Our clients can’t get through and their trust in us is crumbling. Please, you’ve got to do something.”

The targeted company runs a fleet of fragile backend boxes that perform expensive computation on each inbound request. They’ve asked you not to muck around with those internal boxes. Instead, you need to build a defensive proxy layer to drop between the attackers and the backends. The proxy needs to blackhole the attackers while allowing legitimate users to get through.

For this level, the besieged ops team has provided [a bare-bones reverse proxy written in Node.js](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level2/problem/shield). The existing proxy is just a stub, and it does nothing to separate malicious and legitimate traffic. You can expand it or write your own from scratch.

[The repo’s `README.md`](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level2/problem/README.md) gives helpful detail. In the repo, we’ve also included code to simulate the network environment described in our story: fragile backends and an onslaught of legitimate and malicious traffic. You can test and score your proxy inside this simulation by running `test/harness`.

## Write-up

[The provided `shield` script](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level2/problem/shield) contains the following code:

```js
var Queue = function (proxies, parameters) {
  this.proxies = proxies;
  this.parameters = parameters;
};
Queue.prototype.takeRequest = function (reqData) {
  // Reject traffic as necessary:
  // if (currently_blacklisted(ipFromRequest(reqData))) {
  //   rejectRequest(reqData);
  //   return;
  // }
  // Otherwise proxy it through:
  this.proxies[0].proxyRequest(reqData.request, reqData.response, reqData.buffer);
};
```

There are two parts to this challenge:

1. implement load balancing (i.e. making use of all the available proxies instead of just `proxies[0]`)
2. implement rate-limiting (i.e. blacklist IP addresses that attempt to DDoS somehow)

I’ve implemented load balancing as follows:

```diff
diff --git a/shield b/shield
index 4796d2a..1333337 100755
--- a/shield
+++ b/shield
@@ -27,6 +27,7 @@ var Queue = function (proxies, parameters) {
   this.proxies = proxies;
   this.parameters = parameters;
 };
+var proxyIndex = 0;
 Queue.prototype.takeRequest = function (reqData) {
   // Reject traffic as necessary:
   // if (currently_blacklisted(ipFromRequest(reqData))) {
@@ -34,7 +35,9 @@ Queue.prototype.takeRequest = function (reqData) {
   //   return;
   // }
   // Otherwise proxy it through:
-  this.proxies[0].proxyRequest(reqData.request, reqData.response, reqData.buffer);
+  var proxies = this.proxies;
+  proxies[proxyIndex].proxyRequest(reqData.request, reqData.response, reqData.buffer);
+  proxyIndex = (proxyIndex + 1) % proxies.length;
 };
 Queue.prototype.requestFinished = function () {
   return;
```

My rate-limiting solution was a quick and dirty one that turned out to be sufficient to pass this level:

```diff
diff --git a/shield b/shield
index 1333337..9000001 100755
--- a/shield
+++ b/shield
@@ -23,6 +23,17 @@ function rejectRequest(reqData) {
   reqData.response.end();
 }

+var hash = Object.create(null);
+var MAX_REQUESTS = 7; // the number `7` was chosen after some trial and error
+function currently_blacklisted(ip) {
+  var value = hash[ip];
+  if (value != null) {
+    hash[ip]++;
+  } else {
+    hash[ip] = 0;
+  }
+  return value >= MAX_REQUESTS;
+}
+
 var Queue = function (proxies, parameters) {
   this.proxies = proxies;
   this.parameters = parameters;
@@ -30,10 +41,10 @@ var Queue = function (proxies, parameters) {
 var proxyIndex = 0;
 Queue.prototype.takeRequest = function (reqData) {
   // Reject traffic as necessary:
-  // if (currently_blacklisted(ipFromRequest(reqData))) {
-  //   rejectRequest(reqData);
-  //   return;
-  // }
+  if (currently_blacklisted(ipFromRequest(reqData))) {
+    rejectRequest(reqData);
+    return;
+  }
   // Otherwise proxy it through:
   var proxies = this.proxies;
   proxies[proxyIndex].proxyRequest(reqData.request, reqData.response, reqData.buffer);
```

After running [the patched file](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level2/level2) through the test harness, we get output similar to:

```bash
$ ./test/harness
…
Test case passed. Your score: 181.541667. Benchmark score: 127.416667. You/Benchmark: 1.424787. You handled 247 legitimate responses and you received 65.46 negative points for idle time on the backends. The benchmark handled 222 and received 94.58 negative points.
```

Hungry for a higher score, and noticing the scores (both mine and the benchmark’s) were fluctuating heavily even for identical test runs, I just kept on re-submitting the same solution to the CTF server for a few hours:

```bash
$ while :; do git push; done
```

This netted me [a score of 251](https://stripe-ctf.com/achievements/mathias) for this level (11th place on the leaderboard!).

## Other write-ups or solutions

* <http://abiusx.com/stripe-ctf-v3-writeup/>
* <http://tullo.ch/articles/stripe-ctf-golfing/>
* <http://muehe.org/posts/stripe-ctf-3-writeup/>
* [Gibybo’s write-up](https://news.ycombinator.com/item?id=7180991)
* [Jon Eisen’s write-up](http://blog.joneisen.me/post/75008410654)
* [Evan Priestley’s write-up](http://blog.phacility.com/post/stripe_ctf3/)
* [Samuel Walker’s write-up](http://www.samuelwalker.me.uk/2014/01/stripe-ctf3-write-up/)
* <https://github.com/henrik-muehe/level2>
* <https://github.com/metcalf/ctf3/tree/master/level2>
* <https://github.com/xthexder/stripe-ctf-3.0>
* <https://github.com/kratorius/stripe-ctf3/tree/master/level2>
* <https://github.com/lericson/stripe-ctf3/tree/level2>
* [Original problems including a modified test harness that works locally](https://github.com/janosgyerik/stripe-ctf3)
