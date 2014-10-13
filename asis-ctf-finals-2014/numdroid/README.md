# ASIS Cyber Security Contest Finals 2014: Numdroid

**Category:** Reverse Engineering, PPC
**Points:** 150
**Description:**

> Download [file](numdriod_b6394a5e1c13c263bf59397968ef0340) and find the flag!

## Write-up

Let’s see what [the provided file](numdriod_b6394a5e1c13c263bf59397968ef0340) could be:

```bash
$ file numdriod_b6394a5e1c13c263bf59397968ef0340
numdriod_b6394a5e1c13c263bf59397968ef0340: xz compressed data
```

So, we extract the file using the built-in `xz` or `unxz` commands:

* `xz -dc < numdriod_b6394a5e1c13c263bf59397968ef0340 > numdroid`
* `unxz < numdriod_b6394a5e1c13c263bf59397968ef0340 > numdroid`

Alternatively, extract the provided file using [p7zip](http://p7zip.sourceforge.net/):

```bash
7z x numdriod_b6394a5e1c13c263bf59397968ef0340
```

Let’s find out what the extracted file is:

```bash
$ file numdroid
numdroid: Zip archive data, at least v2.0 to extract
```

`numdroid` is actually an Android application package file; feel free to rename it to `numdroid.apk`. `*.apk` files are essentially ZIP files with a different extension. Extracting it reveals (among other things) a `classes.dex` file. `*.dex` files are compiled Android application code files, containing bytecode for the Dalvik Virtual Machine (the workhorse powering the Android system).

Let’s convert the bytecode in the `classes.dex` file back to a `*.jar` file [using `dex2jar`](https://code.google.com/p/dex2jar/):

```bash
$ d2j-dex2jar numdroid.apk
dex2jar numdroid.apk -> numdroid-dex2jar.jar
```

Fun fact: `*.jar` files are essentially zip files too. We can just rename `numdroid-dex2jar.jar` to `numdroid-dex2jar.jar.zip` and unzip it to unpack its contents. Alternatively, this command has the same result:

```bash
$ jar xf numdroid-dex2jar.jar
```

In this case, the resulting source files aren’t easily readable, so let’s use a decompiler. Open `numdroid-dex2jar.jar` in [JD-GUI](http://jd.benow.ca/). Now we can view all the source code, or go to _File_ → _Save All Sources_ to save the sources so we can view them in our preferred text editor.

The source code of the `classes-dex2jar.src/io/asis/ctf2014/numdriod/MainActivity.java` class reveals that the app displays the flag once the correct password is entered:

```java
protected void ok_clicked()
{
  DebugTools.log("clicked password: " + this.mScreen.getText());
  boolean bool = Verify.isOk(this, this.mScreen.getText().toString());
  DebugTools.log("password is Ok? : " + bool);
  if (bool)
  {
    Intent localIntent = new Intent(this, LipSum.class);
    Bundle localBundle = new Bundle();
    localBundle.putString("flag", this.mScreen.getText().toString().substring(0, 7));
    localIntent.putExtras(localBundle);
    startActivity(localIntent);
    return;
  }
  Toast.makeText(this, 2131034114, 1).show();
  this.mScreen.setText("");
}
```

The `Verify.isOk` function is defined in `classes-dex2jar.src/io/asis/ctf2014/numdriod/Verify.java`, and looks like this:

```java
public static boolean isOk(Context paramContext, String paramString)
{
  String str1 = paramString;
  if (paramString.length() > 7)
    str1 = paramString.substring(0, 7);
  String str2 = OneWayFunction(str1);
  DebugTools.log("digest: " + str1 + " => " + str2);
  boolean bool1 = str2.equals("be790d865f2cea9645b3f79c0342df7e");
  boolean bool2 = false;
  if (bool1)
    bool2 = true;
  return bool2;
}
```

So, our input is hashed according to `OneWayFunction`, and if the hashed result equals `be790d865f2cea9645b3f79c0342df7e`, we get the flag. Let’s take a look at `OneWayFunction`:

```java
private static String OneWayFunction(String paramString)
{
  List localList = ArrayTools.map(ArrayTools.select(ArrayTools.map(new String[] { "MD2", "MD5", "SHA-1", "SHA-256", "SHA-384", "SHA-512" }, new MapAction()
  {
    public byte[] action(String paramAnonymousString)
    {
      try
      {
        MessageDigest localMessageDigest = MessageDigest.getInstance(paramAnonymousString);
        localMessageDigest.update(Verify.this.getBytes());
        byte[] arrayOfByte = localMessageDigest.digest();
        return arrayOfByte;
      }
      catch (NoSuchAlgorithmException localNoSuchAlgorithmException)
      {
      }
      return null;
    }
  }), new SelectAction()
  {
    public boolean action(byte[] paramAnonymousArrayOfByte)
    {
      return paramAnonymousArrayOfByte != null;
    }
  }), new MapAction()
  {
    public byte[] action(byte[] paramAnonymousArrayOfByte)
    {
      byte[] arrayOfByte = new byte[8];
      int i = 0;
      if (i >= arrayOfByte.length / 2);
      for (int j = 0; ; j++)
      {
        if (j >= arrayOfByte.length / 2)
        {
          return arrayOfByte;
          arrayOfByte[i] = paramAnonymousArrayOfByte[i];
          i++;
          break;
        }
        arrayOfByte[(j + arrayOfByte.length / 2)] = paramAnonymousArrayOfByte[(-2 + (paramAnonymousArrayOfByte.length - j))];
      }
    }
  });
  byte[] arrayOfByte1 = new byte[8 * localList.size()];
  int i = 0;
  while (true)
  {
    if (i >= arrayOfByte1.length);
    try
    {
      MessageDigest localMessageDigest = MessageDigest.getInstance("MD5");
      localMessageDigest.update(arrayOfByte1);
      byte[] arrayOfByte2 = localMessageDigest.digest();
      StringBuilder localStringBuilder = new StringBuilder();
      int j = arrayOfByte2.length;
      int k = 0;
      if (k >= j)
      {
        String str1 = localStringBuilder.toString();
        return str1;
        arrayOfByte1[i] = ((byte[])localList.get(i % localList.size()))[(i / localList.size())];
        i++;
      }
      else
      {
        String str2;
        for (Object localObject = Integer.toHexString(0xFF & arrayOfByte2[k]); ; localObject = str2)
        {
          if (((String)localObject).length() >= 2)
          {
            localStringBuilder.append((String)localObject);
            k++;
            break;
          }
          str2 = "0" + (String)localObject;
        }
      }
    }
    catch (NoSuchAlgorithmException localNoSuchAlgorithmException)
    {
    }
  }
  return "";
}
```

(TODO)

## Other write-ups

* none yet
