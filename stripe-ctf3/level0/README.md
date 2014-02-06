# Stripe CTF3: level0

## Challenge

Your challenge is to make [this code](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level0/problem/level0) run much faster, without altering its output. In particular, you need to get it running at least as fast as our reference solution — when you submit a revision, we’ll tell you how our solution compares.

## Write-up

[The provided `level0` file](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level0/problem/level0) is a Ruby script that accepts text as input, and then returns that text with any words that are not in the dictionary wrapped in angle brackets.

```ruby
#!/usr/bin/env ruby

# Our test cases will always use the same dictionary file (with SHA1
# 6b898d7c48630be05b72b3ae07c5be6617f90d8e). Running `test/harness`
# will automatically download this dictionary for you if you don't
# have it already.

path = ARGV.length > 0 ? ARGV[0] : '/usr/share/dict/words'
entries = File.read(path).split("\n")

contents = $stdin.read
output = contents.gsub(/[^ \n]+/) do |word|
  if entries.include?(word.downcase)
    word
  else
    "<#{word}>"
  end
end
print output
```

Running [the provided test harness](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level0/problem/test/harness) yields the following output:

```bash
$ ./test/harness
No test case supplied. Randomly choosing among defaults.
Fetching. URL: https://stripe-ctf-3.s3.amazonaws.com/level0/level0-znKqYRKUDB.json
About to run test case: level0-znKqYRKUDB
Beginning run.
Finished run
Test case passed. Your time: 5.291982 seconds. Benchmark time: 0.672016 seconds. You/Benchmark: 7.874785
```

The goal of the level was to make this code more efficient, so that it’s faster than the benchmark.

The improvement that first comes to mind is to use a set or a hash table instead of an array to store the dictionary entries. That way, any lookups can be performed in `O(1)` (constant time).

```diff
diff --git a/level0 b/level0
index f320a7d..1333337 100755
--- a/level0
+++ b/level0
@@ -7,10 +7,11 @@

 path = ARGV.length > 0 ? ARGV[0] : '/usr/share/dict/words'
 entries = File.read(path).split("\n")
+table = Hash[entries.zip(Array.new(entries.size, true))]

 contents = $stdin.read
 output = contents.gsub(/[^ \n]+/) do |word|
-  if entries.include?(word.downcase)
+  if table[word.downcase]
     word
   else
     "<#{word}>"
```

[This solution](https://github.com/ctfs/write-ups/blob/master/stripe-ctf3/level0/level0) is already faster than the reference solution:

```bash
$ ./test/harness
No test case supplied. Randomly choosing among defaults.
About to run test case: level0-znKqYRKUDB
Beginning run.
Finished run
Test case passed. Your time: 0.254984 seconds. Benchmark time: 0.672016 seconds. You/Benchmark: 0.379432
```

Level solved!

For more points, you could implement a [trie](http://en.wikipedia.org/wiki/Trie) data structure such as a [MARISA trie](https://code.google.com/p/marisa-trie/) to store the dictionary entries.

## Other write-ups or solutions

* <http://abiusx.com/stripe-ctf-v3-writeup/>
* <http://tullo.ch/articles/stripe-ctf-golfing/>
* <http://muehe.org/posts/stripe-ctf-3-writeup/>
* [Gibybo’s write-up](https://news.ycombinator.com/item?id=7180991)
* [Jon Eisen’s write-up](http://blog.joneisen.me/post/75008410654)
* [Evan Priestley’s write-up](http://blog.phacility.com/post/stripe_ctf3/)
* [Samuel Walker’s write-up](http://www.samuelwalker.me.uk/2014/01/stripe-ctf3-write-up/)
* [@paraboul’s 3rd place solution](https://gist.github.com/paraboul/8735537)
* <https://github.com/henrik-muehe/level0>
* <https://github.com/metcalf/ctf3/tree/master/level0>
* <https://github.com/xthexder/stripe-ctf-3.0>
* <https://github.com/vinzenz/stripe-ctf3-solutions/tree/master/level0>
* <https://github.com/kratorius/stripe-ctf3/tree/master/level0>
* <https://github.com/lericson/stripe-ctf3/tree/level0>
* [Original problems including a modified test harness that works locally](https://github.com/janosgyerik/stripe-ctf3)
