# Qiwi CTF 2014: Stolen prototype

**Category:** Misc
**Points:** 100
**Author:** tracer0tong
**Description:**

> This is a [stolen application](android100.apk) of super-duper payment system.
>
> But this is broken piece of cake, completely broken =(

## Write-up

[The provided `android100.apk` file](android100.apk) is an Android application package file. `*.apk` files are essentially ZIP files with a different extension. Extracting it reveals (among other things) a `classes.dex` file. `*.dex` files are compiled Android application code files, containing bytecode for the Dalvik Virtual Machine (the workhorse powering the Android system).

Let’s convert the bytecode in the `classes.dex` file back to a `*.jar` file [using `dex2jar`](https://code.google.com/p/dex2jar/):

```bash
$ d2j-dex2jar android100.apk
dex2jar android100.apk -> android100-dex2jar.jar
```

Fun fact: `*.jar` files are essentially ZIP files too. We can just rename `numdroid-dex2jar.jar` to `numdroid-dex2jar.jar.zip` and unzip it to unpack its contents. Alternatively, this command has the same result:

```bash
$ jar xf android100-dex2jar.jar
```

In this case, the resulting source files aren’t easily readable, so let’s use a decompiler. Open `android100-dex2jar.jar` in [JD-GUI](http://jd.benow.ca/). Now we can view all the source code, or go to _File_ → _Save All Sources_ to save the sources so we can view them in our preferred text editor.

The source code of the `com/mslc/ctf/piwiotp/Account.java` class reveals that the app makes an HTTP request. Here’s the code with added comments:

```java
private String a() {
  Character localCharacter = Character.valueOf('n'); // 'n'
  String str1 = this.d.substring(0, 1); // 'h'
  Log.d(getPackageName(), str1);
  // → D/com.mslc.ctf.piwiotp(15685): h
  StringBuilder localStringBuilder = new StringBuilder();
  DefaultHttpClient localDefaultHttpClient = new DefaultHttpClient();
  String str2 = str1 + "vty"; // 'hvty'
  Log.d(getPackageName(), localCharacter + "s" + str2 + "f" + localCharacter + "j" + str1);
  // → D/com.mslc.ctf.piwiotp(15685): nshvtyfnjh

  UsernamePasswordCredentials localUsernamePasswordCredentials = new UsernamePasswordCredentials("xxx", localCharacter + "s" + str2 + "f" + localCharacter + "j" + str1);
  // → username is `xxx` and password is `nshvtyfnjh`

  HttpGet localHttpGet = new HttpGet("https://qiwictf2014.ru:54321/account?key=" + "" + "&account=" + "afgssdfgsdgsfgdfbxcbsdbkjnkwej");
  try {
    localHttpGet.addHeader(BasicScheme.authenticate(localUsernamePasswordCredentials, "UTF-8", false));
    HttpResponse localHttpResponse = localDefaultHttpClient.execute(localHttpGet);
    if (localHttpResponse.getStatusLine().getStatusCode() == 200) {
      // …
    }
  } catch (…) {
    // …
  }
}
```

Note that any calls to `Log.d()` can be inspected while running the app by using [`adb logcat`](https://developer.android.com/tools/help/logcat.html).

As the challenge description indicates, the app is broken: the HTTP request fails, and therefore the response is never displayed. Let’s recreate the request and see what we can do about that.

The above code reveals that a request is made to `https://qiwictf2014.ru:54321/account?key=&account=afgssdfgsdgsfgdfbxcbsdbkjnkwej` using Basic Authentication with username `xxx` and password `nshvtyfnjh`.

```bash
$ curl -u 'xxx:nshvtyfnjh' 'https://qiwictf2014.ru:54321/account?key=&account=afgssdfgsdgsfgdfbxcbsdbkjnkwej'
curl: (7) Failed to connect to qiwictf2014.ru port 54321: Connection refused
```

Elsewhere in the code, we find another port on the same host:

```java
protected void onCreate(Bundle paramBundle) {
  super.onCreate(paramBundle);
  StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().permitAll().build());
  Random localRandom = new Random();
  String str = "ctf201" + "444444".charAt(localRandom.nextInt("444444".length()));
  // Note the next line:
  this.d = ("https://qiwi" + str + ".ru:" + "40443");
  setContentView(2130903040);
  this.b = ((TextView)findViewById(2131230723));
  this.c = ((Button)findViewById(2131230728));
  this.c.setOnClickListener(new a(this));
  Log.d(getPackageName(), "Init for:https://qiwictf2014.ru:54321" + a());
}
```

So let’s try accessing port `40443` instead:

```bash
$ curl -u 'xxx:nshvtyfnjh' 'https://qiwictf2014.ru:40443/account?key=&account=afgssdfgsdgsfgdfbxcbsdbkjnkwej'
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```

Hmm, we still get an error, but at least the connection succeeds. Let’s request the main page (`/`):

```bash
$ curl -u 'xxx:nshvtyfnjh' 'https://qiwictf2014.ru:40443/'
{"status": 405, "message": "Method Not Allowed"}
```

Since `GET` is not allowed, let’s try `POST`:

```bash
$ curl -X POST -u 'xxx:nshvtyfnjh' 'https://qiwictf2014.ru:40443/'
{"welldone": "ZN2014_3db056df7036e11c823707f5adf923e9"}
```

The flag is `ZN2014_3db056df7036e11c823707f5adf923e9`.

## Other write-ups and resources

* <http://nandynarwhals.org/2014/11/14/qiwictf2014-stolen-prototype-misc100/>
