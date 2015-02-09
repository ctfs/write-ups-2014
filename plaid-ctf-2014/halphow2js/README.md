# Plaid CTF 2014: halphow2js

**Category:** Web
**Points:** 200
**Description:**

> Javascript is everywhere. But there is [one strange javascript blob](https://54.196.246.17:8001/) we have been seeing pop up on servers throughout the ages. We're pretty sure The Plague must be involved.
>
> Note: we know the cert displays a warning - that isn't important.

## Write-up

[The HTML source for the website linked to in the description](index.html) reveals [`script.js`](script.js), a polyglot JavaScript file that runs in both the browser and in Node.js.

Reading through the code makes it clear that the client-side section of the script prompts the user for input five times, and then submits that data to the server. If the input matches certain conditions, the flag is returned, else, the process starts over.

The data is sent using a GET request to `https://54.196.246.17:8001/myajax?x=1&y=2&z=3&w=4&ww=5`. The server-side section of the script validates these URL query string parameters as follows: if `FLAG` (a value unknown to us) is equal to `filter(query.x, query.y, query.z, query.w, query.ww)`, then the flag is revealed.

Let’s take a closer look at that `filter` function:

```js
function filter() {
  var args = [].slice.apply(arguments).sort().filter(function(x, i, a) {
    return a.indexOf(x) == i;
  });
  if (args.length != 5) return "uniq";

  var flag = false;
  args.map(function(x) {
    flag |= x >= 999;
  });
  if (flag) return "big";

  var m = args.map(mystop);

  if (m.filter(function(x, i) { return m[2] + 3 * i == x; }).length < 3) {
    return "unsexy";
  }
  if (m.filter(function(x, i) { return x == args[i]; }).length < 3) {
    return "hippopotamus";
  }
  if (m.filter(function(x, i) { return x > m[i-1]; }).length > 3) {
    return "banana phone";
  }

  return FLAG;
}
```

We can make the following observations:

* First, the arguments are lexicographically sorted. This effectively means that `?x=1&y=2&z=3&w=4&ww=5` and `?x=5&y=4&z=3&w=2&ww=1` have the same effect, which reduces the number of combinations to test in a brute-force scenario.
* It takes exactly five unique arguments. If not, the function exits early, and we won’t get to the flag. Once again, this makes brute-forcing a bit easier.
* If for any of the arguments `x` the expression `x >= 999` holds true, the function exits early, and we won’t get to the flag.
* `mystop(x)` is then called for each argument `x`, which can take several minutes depending on the value of `x`. The resulting list of arguments (`m`) must match certain conditions, else the function exits early, and we won’t get to the flag.

At this point it’s tempting to start bruteforcing by sending all possible sets of five numeric values below `999` to the server. That’s several trillions of possible combinations, though… It also doesn’t help that the server-side code only sends a response after at least 2 seconds. Brute-forcing is not exactly feasible for this challenge.

Remember the `query.x`, `query.y`, `query.z`, `query.w`, and `query.ww` values that are validated on the server-side? [They’re string values](http://nodejs.org/api/querystring.html#querystring_querystring_parse_str_sep_eq_options), and the script never explicitly casts them into numbers. This means we can pick any string values `x` for the parameters, as long as `x >= 999` evaluates to `false`.

So instead of trying to find the perfect combination of numbers, we can just pick any five strings that can be coerced into numbers, and then format them in different ways until all validation checks are passed. For example, the number `5` can also be written as `5.`, `5.0`, `5.00`, or `5e0` in JavaScript. And because the values are strings that are coerced to numbers (equivalent to `Number(string)`) we can even pad the values with whitespace, e.g. `" 5"` or `"5 "` instead of `"5"`.

After some manual fiddling with various numbers and formats, we found a working set of values:

```js
// This code assumes the `filter` function and its dependencies are declared as
// in the provided `script.js`.
var FLAG = 'Congratulations!';
console.log(filter('2.0', '2.00', '2.000', '7', '76'));
// → 'Congratulations!'
```

Now we can open <https://54.196.246.17:8001/> and enter the values one by one, after which the flag is shown in an alert box. But using `curl` is simpler:

```bash
$ curl --insecure 'https://54.196.246.17:8001/myajax?x=2.0&y=2.00&z=2.000&w=7&ww=76'
w00t_i_are_mastar_web_hackar
```

The flag is `w00t\_i\_are\_mastar\_web\_hackar`.

## Other write-ups and resources

* <http://balidani.blogspot.com/2014/04/plaidctf-halphow2js-writeup.html>
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/web/halphow2js)
* <http://j00ru.vexillium.org/dump/ctf/halphow2js.txt>
