# DEFKTHON CTF: Web 300

**Description:**

> [we love it!](web300.apk)

## Write-up

We’re given an Android application package file, [`web300.apk`](web300.apk). `*.apk` files are essentially zip files with a different extension. If you rename it to `web300.apk.zip` and extract it, you’ll see it contains a `classes.dex` file. `*.dex` files are compiled Android application code files, containing bytecode for the Dalvik Virtual Machine (the workhorse powering the Android system).

Let’s convert the bytecode in the `classes.dex` file back to a `*.jar` file [using `dex2jar`](https://code.google.com/p/dex2jar/):

```bash
$ d2j-dex2jar web300.apk
dex2jar web300.apk -> web300-dex2jar.jar
```

Now, `\*.jar` files are essentially zip files too. We can just rename `web300-dex2jar.jar` to `web300-dex2jar.jar.zip` and unzip it to unpack its contents. Alternatively, this command has the same result:

```bash
$ jar xf web300-dex2jar.jar
```

In this case, the resulting source files aren’t easily readable, so let’s use a decompiler. Open `web300-dex2jar.jar` in [JD-GUI](http://jd.benow.ca/). Now we can view all the source code, or go to _File_ → _Save All Sources_ to save the sources so we can view them in our preferred text editor.

The `com.example.defkthonapp/MainActivity` class looks interesting:

```java
private Runnable Check = new Runnable()
{
  public void run()
  {
    TelephonyManager localTelephonyManager = (TelephonyManager)MainActivity.this.getSystemService("phone");
    String str1 = localTelephonyManager.getDeviceId();
    String str2 = localTelephonyManager.getSimSerialNumber();
    int i = new Random().nextInt(300);
    ((WebView)MainActivity.this.findViewById(2131230723)).postUrl("http://challenges.defconkerala.com/web/300/update.php", EncodingUtils.getBytes("pwd=" + Integer.toString(i) + "&imei=" + str1 + "&div=" + str2, "BASE64"));
  }
};
private EditText paswd;
```

So, the app performs a POST request to `http://challenges.defconkerala.com/web/300/update.php` with `pwd=$password&imei=$deviceID&div=$simSerialNumber` as POST data. The `$deviceID` and `$simSerialNumber` never change for the same device, only the `$password` does — and it is a random integer from 0 (inclusive) to 300 (exclusive).

Testing reveals that the `$deviceID` and `$simSerialNumber` aren’t validated in any way on the server, so we can just use bogus values for them. The `User-Agent` request header seems to be checked though — if it doesn’t contain `Android`, the following response is sent:

```
We love android !!
```

Setting `_Android` as the `User-Agent` header seems to work.

Let’s brute-force the password and see what happens. I wrote a quick shell script for this:

```bash
#!/usr/bin/env bash

deviceID='1337';
simSerialNumber='1337';
user_agent='_Android';

url='http://challenges.defconkerala.com/web/300/update.php';

for password in {0..299}; do
  data="pwd=${password}&imei=${deviceID}&div=${simSerialNumber}";
  curl -s --user-agent "${user_agent}" --data "${data}" "${url}" | grep 'Flag';
done;
```

Let’s run it:

```bash
$ ./web300.sh
Flag is: w00tkitk@t
```

The flag is `w00tkitk@t`.

## Other write-ups and resources

* <http://blog.0xdeffbeef.com/2014/03/defkthon-ctf-2014-we-love-it-web-300.html>
* <http://tasteless.eu/2014/03/defkthon-ctf-2014-web200-web300-and-web400-writeup/>
* [Japanese](http://wataamectf.blogspot.jp/2014/03/defkthon-ctf-writeup.html)
