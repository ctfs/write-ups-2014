# DEFKTHON CTF: Reversing 100

**Description:**

> [Hackers are Here](100.exe)

## Write-up

_This write-up is made by the [HacknamStyle](http://hacknamstyle.net/) CTF team._

First we want to know the type of file we are dealing with. On Linux `file 100.exe` returns that it's a .NET assembly. If you open it in IDA you will also be told it's a .NET program. For a bit of background, there's also [TrID](http://mark0.net/soft-trid.html) to identify file types, [PROTECTiON iD](http://pid.gamecopyworld.com/) to detect binary packets, the older [PEiD](http://www.aldeid.com/wiki/PEiD), etc.

I used [IDA](https://www.hex-rays.com/products/ida/) to view the .NET intermediate language instructions, and [JetBrains dotPeek](http://www.jetbrains.com/decompiler/) to disassemble the code. After removing all useless code dotPeek shows the following:

```
private void pictureBox1_Click(object sender, EventArgs e)
{
  try
  {
    int num1 = (int) MessageBox.Show([...]);
    int num2 = 1337;
    int num3 = 0;
    int num4 = int.Parse(string.Concat(new object[4]
    {
      (object) "121299999999999999999999999999999999999B0wB4me4iamr",
      (object) num3,
      (object) num3,
      (object) "t99999999999999999999999999999999999999"
    }));
    string str = (string) (object) num2 + (object) num4.ToString();
    for (int index = 0; index <= num4; ++index)
      num4 = num4 + (num2 ^ 1337) + num2 * 2000 / 1337 / 1337 / 24;
    this.Usehint();
  }
  catch { }
}

public void Usehint() { }

private void InitializeComponent()
{
  [...]
  this.label1.Location = new Point(701, 242);
  this.label1.Text = "      key is md5(sha1)";
  [...]
}
```

We see the hint `key is md5(sha1)`, which is not visible when running the program because the position of the label is outside the window. So we need to find a key and calculate the MD5 and SHA1 hash of it. Though the `Usehint()` function appears empty, in IDA we can see that it actually loads a string but does nothing with it:

```
.method public hidebysig instance void Usehint() // CODE XREF: pictureBox1_Click
{
  .maxstack 1
  .locals init (string V0)
  nop
  ldstr    "get_key_from_hint"
  stloc.0
  ret
}
```

So the last place to look for this hint is the horribly coded `pictureBox1_Click` function. Do we somehow have to fix this function and run it? Because now it throws exceptions. Staring at it a bit longer, the string constructed by the program contains `B0wB4me4iamr00t`. This is the key. I know, it doesn’t make much sense…

The solution becomes:

```bash
$ echo -n "B0wB4me4iamr00t" | sha1sum
9df54a6411ed678cdc925b26794052a882830c25  -
echo -n "9df54a6411ed678cdc925b26794052a882830c25" | md5sum
58b4d49e5489be09fc409e4c0b5e66ad
```

The solution is `58b4d49e5489be09fc409e4c0b5e66ad`.

## Other write-ups and resources

* <http://ctfwriteups.blogspot.in/2014/03/defkthon-2014-reversing-100.html>
