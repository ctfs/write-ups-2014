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

The `ctf/crackme` directory looks interesting.

(TODO)

## Other write-ups

* none yet
