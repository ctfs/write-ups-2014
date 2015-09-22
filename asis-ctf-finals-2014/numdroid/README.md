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

Let’s install `numdroid.apk` onto an Android device (or emulator):

```bash
$ adb install numdroid.apk
```

The app seems to be looking for a password consisting of up to 7 numerical digits. This can be solved using brute force directly on a fairly recent smartphone. In order to do so, the APK has to be modified to test every combination, instead of only the one entered in the text field.

The easiest way to modify an APK is with [APK studio](http://forum.xda-developers.com/showthread.php?t=2493107). A quick scan through the files reveals calls to the `DebugTools.log()` method. However, `logcat` does not display any logs from the `apk`. A quick look at the `DebugTools` class reveals the following:

```
# direct methods
.method static constructor <clinit>()V
  .locals 1

  .prologue
  .line 6
  const-string v0, "Numdroid"

  sput-object v0, Lio/asis/ctf2014/numdriod/tools/DebugTools;->DBG_TAG:Ljava/lang/String;

  .line 7
  const/4 v0, 0x0

  sput-boolean v0, Lio/asis/ctf2014/numdriod/tools/DebugTools;->DBG:Z

  return-void
```

By changing the `DBG` flag to `0x1` in the constructor (line 23 in `DebugTools.smali`), all debug calls are forwarded to `logcat`.

The code that is executed when the ‘go’ button is pressed can be found in `MainActivity.smali` (line 339).

```
  .line 77
  iget-object v3, p0, Lio/asis/ctf2014/numdriod/MainActivity;->mScreen:Landroid/widget/EditText;

  invoke-virtual {v3}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

  move-result-object v3

  invoke-interface {v3}, Landroid/text/Editable;->toString()Ljava/lang/String;

  move-result-object v3

  invoke-static {p0, v3}, Lio/asis/ctf2014/numdriod/Verify;->isOk(Landroid/content/Context;Ljava/lang/String;)Z

  move-result v2
```

A single string is sent to the `Verify.isOk` method. The easiest (laziest?) way to modify this to a bruteforce is coding a bruteforce in Java, then copying over the resulting Dalvik codes. I made the Java code similar to the Numdroid code to minimize the required modifications:

```java
@Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    if (savedInstanceState == null) {
      getSupportFragmentManager().beginTransaction()
          .add(R.id.container, new PlaceholderFragment()).commit();
    }

    for(int i = 0; i< 9999999; i++)
    {
      boolean ok = MainActivity.isOk(Integer.toString(i));
      if(i % 100000 == 0)
      {
        log(Integer.toString(i));
      }
      if(ok)
      {
        log(Integer.toString(i));
      }
    }
  }

  public void log(String str)
  {
    //do something
  }

  public static boolean isOk(String str)
  {
    return true;
  }
```

Which translates to…

```
.line 26
  :cond_0
  const/4 v0, 0x0

  .local v0, "i":I
  :goto_0
  const v2, 0x98967f

  if-lt v0, v2, :cond_1

  .line 38
  return-void

  .line 28
  :cond_1
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2

  invoke-static {v2}, Lcom/example/forloop/MainActivity;->isOk(Ljava/lang/String;)Z

  move-result v1

  .line 29
  .local v1, "ok":Z
  const v2, 0x186a0

  rem-int v2, v0, v2

  if-nez v2, :cond_2

  .line 31
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2

  invoke-virtual {p0, v2}, Lcom/example/forloop/MainActivity;->log(Ljava/lang/String;)V

  .line 33
  :cond_2
  if-eqz v1, :cond_3

  .line 35
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2

  invoke-virtual {p0, v2}, Lcom/example/forloop/MainActivity;->log(Ljava/lang/String;)V

  .line 26
  :cond_3
  add-int/lit8 v0, v0, 0x1

  goto :goto_0
```

In order to paste this into the `Numdroid.apk`, some changes have to be made. The Numdroid code already contains a `cond_0` and a `goto_0` so our code has to be changed to use `:goto_1` and `:cond_4`. Lastly, the method names have to be changed, resulting in the following:

```
  const/4 v0, 0x0

  .local v0, "i":I
  :goto_3
  const v2, 0x98967f

  if-lt v0, v2, :cond_3
  return-void

  .line 28
  :cond_3
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2

  invoke-static {p0, v2}, Lio/asis/ctf2014/numdriod/Verify;->isOk(Landroid/content/Context;Ljava/lang/String;)Z

  move-result v1

  .line 29
  .local v1, "ok":Z

   const v4, 0x186a0

  rem-int v4, v0, v4

  if-nez v4, :cond_6

  .line 31
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2
  invoke-static {v2}, Lio/asis/ctf2014/numdriod/tools/DebugTools;->log(Ljava/lang/String;)V

  :cond_6

  if-eqz v1, :cond_2

  goto :goto_4
  .line 31
  invoke-static {v0}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

  move-result-object v2

  invoke-static {v2}, Lio/asis/ctf2014/numdriod/tools/DebugTools;->log(Ljava/lang/String;)V

  .line 26
  :cond_2
  add-int/lit8 v0, v0, 0x1

  goto :goto_3
```

APK Studio can then recompile the `apk` and you can install it using `adb install numdroid.apk`. Be aware that the certificate used to sign the modified `apk` is different from the original one, so you have to uninstall the original application first.

My Galaxy S4 smartphone tries about 100,000 combinations per minute, so it could take 1.5 hours to try all the combinations. That’s a lot slower than my computer would do it, but it’s still fast enough.

After some time, the correct code is found (`3130110`) and the following message is shown:

> The Flag is: `ASIS_{MD5(3130110)}`

`md5(3130110)` is `3c56e1ed0597056fef0006c6d1c52463`, so the flag is `ASIS_3c56e1ed0597056fef0006c6d1c52463`.

That was a lot more fun than just running the Java code on my computer ;).

## Other write-ups and resources

* <http://tasteless.eu/2014/10/asis-ctf-finals-2014-numdroid/>
