# tinyCTF 2014: NaNNaNNaNNaN…, Batman!

**Category:** Web
**Points:** 100
**Description:**

> [Download file](web100.zip)

## Write-up

Let’s unzip [the provided `web100.zip` file](web100.zip):

```bash
$ unzip web100.zip
Archive:  web100.zip
  inflating: web100
```

The extracted `web100` file is an HTML document that contains a script. The script is obfuscated and contains control characters. Here’s a (believe it or not) cleaned up version:

```js
_ = 'function $(){\x02e=\x04getEle\x0FById("c").value;\x0Elength==16\x05^be0f23\x01233ac\x01e98aa$\x01c7be9\x07){\x02t\bfl\x03s_a\x03i\x03e}\x06n\ba\x03_h0l\x03n\x06r\bg{\x03e\x03_0\x06i\bit\'\x03_\x03n\x06s=[t,n,r,i];for(\x02o=0;o<13;++o){\t\x0B[0]);\x0B.splice(0,1)}}}\t\'<input id="c"><\f onclick=$()>Ok</\f>\');delete _\x01\x07\x05\x02var \x03","\x04docu\x0F.\x05)\x0Ematch(/\x06"];\x02\x07/)!=null\b=["\t\x04write(\x0Bs[o%4]\fbutton\x0Eif(e.\x0Fment';
for (Y in $ = '\x0F\x0E\f\x0B\t\b\x07\x06\x05\x04\x03\x02\x01')
  with (_.split($[Y]))
    _ = join(pop());
eval(_);
```

To see what code gets evaluated, let’s replace the `eval` at the end with `console.log`. This results in:

```js
function $(){var e=document.getElementById("c").value;if(e.length==16)if(e.match(/^be0f23/)!=null)if(e.match(/233ac/)!=null)if(e.match(/e98aa$/)!=null)if(e.match(/c7be9/)!=null){var t=["fl","s_a","i","e}"];var n=["a","_h0l","n"];var r=["g{","e","_0"];var i=["it'","_","n"];var s=[t,n,r,i];for(var o=0;o<13;++o){document.write(s[o%4][0]);s[o%4].splice(0,1)}}}document.write('<input id="c"><button onclick=$()>Ok</button>');delete _
```

This beautifies into:

```js
function $() {
  var e = document.getElementById('c').value;
  if (e.length == 16) {
    if (e.match(/^be0f23/) != null) {
      if (e.match(/233ac/) != null) {
        if (e.match(/e98aa$/) != null) {
          if (e.match(/c7be9/) != null) {
            var t = ['fl', 's_a', 'i', 'e}'];
            var n = ['a', '_h0l', 'n'];
            var r = ['g{', 'e', '_0'];
            var i = ['it\'', '_', 'n'];
            var s = [t, n, r, i];
            for (var o = 0; o < 13; ++o) {
              document.write(s[o % 4][0]);
              s[o % 4].splice(0, 1);
            }
          }
        }
      }
    }
  }
}
document.write('<input id="c"><button onclick=$()>Ok</button>');
delete _;
```

From this code, we can tell we’re supposed to enter a value into a text field. If this value matches certain conditions, another value (possibly the flag) will be printed. Here’s what we know about the expected input:

* it contains exactly 16 characters (`e.length == 16`)
* it starts with `be0f23` (`e.match(/^be0f23/) != null`)
* it ends with `e98aa` (`e.match(/e98aa$/) != null`)
* it contains `233ac` (`e.match(/233ac/) != null`)
* it contains `c7be9` (`e.match(/e98aa$/) != null`)

There’s only one string that satisfies all these requirements: `be0f233ac7be98aa`.

Entering it reveals the flag:

```
flag{it's_a_h0le_in_0ne}
```

### Alternate solution

Since the code that is executed once the correct value is entered doesn’t depend on the actual input, you could just run it directly:

```js
var t = ['fl', 's_a', 'i', 'e}'];
var n = ['a', '_h0l', 'n'];
var r = ['g{', 'e', '_0'];
var i = ['it\'', '_', 'n'];
var s = [t, n, r, i];
for (var o = 0; o < 13; ++o) {
  document.write(s[o % 4][0]);
  s[o % 4].splice(0, 1);
}
```

This prints the flag.

## Other write-ups and resources

* <https://github.com/jesstess/tinyctf/blob/master/batman/batman.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/.
