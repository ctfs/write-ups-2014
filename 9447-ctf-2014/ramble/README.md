# 9447 CTF 2014: ramble

**Category:** Web
**Points:** 200
**Solves:** 58
**Description:**

> [travels of a lonely cloud](http://ramble.9447.plumbing:8888/)
>
> [`server.js`](server.js)
>
> **Hint!** JS has interesting scoping properties…

## Write-up

[The website](http://ramble.9447.plumbing:8888/) is a photolog, available in two languages. The URL parameter `?lang=en_US` is the implied default; `?lang=fr_FR` is the other option.

[The provided source code](server.js) contains some filtering logic that is intended to prevent the use of other locales.

[The `filterOptions` function](https://github.com/ctfs/write-ups/blob/master/9447-ctf-2014/ramble/server.js#L56-L83) iterates over each URL parameter (sorted lexicographically), and calls `filterValidLanguages()` if the parameter name lowercases to `'lang'`:

```js
function filterOptions(params) {
  var options = {}

  var sorted_param_names = Object.keys(params).sort();
  var params_processed = 0;
  for (i = 0; i < sorted_param_names.length; i++) {
    var lowered = sorted_param_names[i].toLowerCase();

    if (lowered == 'lang') {
      filterValidLanguages(params, lowered);
      options['lang'] = params[sorted_param_names[i]];
      params_processed++;
    // } else if (lowered == 'paginationnumposts') {
    //   param = params[sorted_param_names[i]];
    //   if (parseInt(param) > 0) {
    //     options['pagination_num_posts'] = parseInt(param);
    //     params_processed++;
    //   }
    } else {
      // Track user activity, so we can see where they go
      options['usertoken'] = params[sorted_param_names[i]];
      params_processed++;
    }

    if (params_processed >= 3) return options;
  }
  return options;
}
```

Note that he variable `i` is never declared using `var`; it is an implicit global variable.

`filterValidLanguages` makes use of the same implicit global variable `i`:

```js
function filterValidLanguages(params, param_name) {
  // Russian doesn't work on this server for some reason?
  // LANGUAGES = ['fr_FR', 'en_US', 'ru_RU']
  var LANGUAGES = ['fr_FR', 'en_US']
  for (i = 0; i < LANGUAGES.length; i++) {
    if (params[param_name] == LANGUAGES[i]) return;
  }
  params[param_name] = 'en_US';
  return;
}
```

This presents a subtle vulnerability: at the start of the first loop iteration in `filterOptions`, `i` equals `0`. If, after sorting the URL parameter names lexicographically, the first URL parameter name lowercases to `'lang'`, the `if (lowered == 'lang')` branch is entered, and the following code is run:

```js
filterValidLanguages(params, lowered);
// Note: from now on, `i` is `2` instead of `0`!
options['lang'] = params[sorted_param_names[i]];
params_processed++;
```

After the `filterValidLanguages` call, the value of `i` is `2`, although the code expects it to be the same value it had before (`0` in this case). So, the value stored in `options['lang']` is not the value for the URL parameter, but rather the value for the third URL parameter name in the sorted list.

This means we can bypass the “valid language” filter, and set the language to any value we like, e.g. `ru_RU.UTF-8`, by constructing a query string similar to this:

```
?lang=x&y=a&z=ru_RU.UTF-8
```

[The `getPosts` function](https://github.com/ctfs/write-ups/blob/master/9447-ctf-2014/ramble/server.js#L85-L118) assigns the language (which we can now control) to the `LC_ALL` environment variable, and spawns a shell that executes `ls -l $some_hardcoded_directory_value_we_cannot_control`. Could this be a case of [Shellshock](https://en.wikipedia.org/wiki/Shellshock_%28software_bug%29#Initial_report_.28CVE-2014-6271.29)?

Below are some possible ways to successfully exploit this challenge.

## Other write-ups and resources

* <http://tasteless.eu/2014/12/9447-security-society-ctf-2014-ramble-writeup/>
* [Exploit by Ymgve that leaks `/flag` piece by piece](https://gist.github.com/anonymous/fa48e7657ddf9d4f9d6d)
* [Exploit by HoLyVieR using a timing attack + blind Shellshock injection](https://gist.github.com/jghkdgha/0a40941cdb072bfe269f)
* [Exploit by cyberguru - execute command with one query](http://pastebin.com/nGGTNt6K)
