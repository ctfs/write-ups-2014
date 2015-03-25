# tinyCTF 2014: Ooooooh! What does this button do?

**Category:** Reverse Engineering
**Points:** 200
**Description:**

> [Download file](rev200.zip)

## Write-up

Let’s unzip [the provided `rev200.zip` file](rev200.zip):

```bash
$ unzip rev200.zip
Archive:  rev200.zip
  inflating: rev200
```

The extracted `rev200` file is another ZIP file:

```bash
$ unzip rev200
Archive:  rev200
  inflating: res/layout/activity_flag.xml
  inflating: res/layout/activity_main.xml
  inflating: res/menu/flag.xml
  inflating: res/menu/main.xml
  inflating: AndroidManifest.xml
  inflating: resources.arsc
  inflating: res/drawable-hdpi/ic_launcher.png
  inflating: res/drawable-mdpi/ic_launcher.png
  inflating: res/drawable-xhdpi/ic_launcher.png
  inflating: res/drawable-xxhdpi/ic_launcher.png
  inflating: classes.dex
  inflating: META-INF/MANIFEST.MF
  inflating: META-INF/CERT.SF
  inflating: META-INF/CERT.RSA
```

Well, actually, it might’ve been an Android application package file (`*.apk`).

Anyway, let’s convert the bytecode in the `classes.dex` file back to a `*.jar` file [using `dex2jar`](https://code.google.com/p/dex2jar/):

```bash
$ d2j-dex2jar classes.dex
dex2jar classes.dex -> classes-dex2jar.jar
```

Fun fact: `*.jar` files are essentially zip files too. We can just rename `classes-dex2jar.jar` to `classes-dex2jar.jar.zip` and unzip it to unpack its contents. Alternatively, this command has the same result:

```bash
$ jar xf classes-dex2jar.jar
```

In this case, the resulting source files aren’t easily readable, so let’s use a decompiler. Open `classes-dex2jar.jar` in [JD-GUI](http://jd.benow.ca/). Now we can view all the source code, or go to _File_ → _Save All Sources_ to save the sources so we can view them in our preferred text editor.

The `ctf/crackme` directory looks interesting. The `FlagActivity.java` file contains:

```java
protected void onCreate(Bundle paramBundle)
{
  super.onCreate(paramBundle);
  setContentView(2130903040);
  String str = "";
  int[] arrayOfInt = { 102, 108, 97, 103, 123, 119, 52, 110, 110, 52, 95, 106, 52, 114, 95, 109, 121, 95, 100, 51, 120, 125 };
  for (int i = 0; ; i++)
  {
    if (i >= 22)
    {
      ((TextView)findViewById(2131230721)).setText(str);
      return;
    }
    str = str.concat(String.valueOf((char)arrayOfInt[i]));
  }
}
```

The above snippet builds a string based on an array of Unicode code points. Let’s see what string it creates:

```js
$ node -e 'console.log(String.fromCharCode(102, 108, 97, 103, 123, 119, 52, 110, 110, 52, 95, 106, 52, 114, 95, 109, 121, 95, 100, 51, 120, 125));'
flag{w4nn4_j4r_my_d3x}
```

The flag is `flag{w4nn4_j4r_my_d3x}`.

## Other write-ups and resources

* <https://github.com/evanowe/TinyCTF2014-writeups/blob/master/README.md#ooooooh-what-does-this-button-do>
* <http://sugarstack.io/tinyctf-rev-200.html>
* <https://github.com/jesstess/tinyctf/blob/master/button/button.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/>
