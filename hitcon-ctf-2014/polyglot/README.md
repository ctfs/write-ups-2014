# HITCON CTF 2014: polyglot

**Category:** Crazy
**Points:** 500
**Description:**

> Just `cat flag`
> http://210.61.2.47:8192/

**Hint:**

> Similar to DEFCON 22 quals polyglot, but ...
>
> Judge command:
>
> ```bash
> /usr/bin/python2.7 temp.py 2>/dev/null
> /usr/bin/python3.4 temp.py 2>/dev/null
> /usr/bin/gcc temp.c -o tempexe 2>/dev/null && tempexe 2>/dev/null
> /usr/bin/ruby temp.rb 2>/dev/null
> /usr/bin/runhaskell temp.hs 2>/dev/null
> ```

## Write-up

<https://gist.github.com/pyrocat101/c1c300c4d806513c1a56>

We start from Python2/3:

```python
import os
os.system("cat flag");
```

To make `gcc` happy, we need some polyglot syntax to comment out the `import` statement in C. Recall that C has compiler directives that start with `#`, which is also a line comment in Python. Conditional compilation seems to be an ideal choice because it also acts as a block comment in C. Then we can define a macro for `main` so that the result is valid in Python and in C.

```c
#if 0
import os
p = os.system
#endif
#define p(s) main(){system(s);}
p("cat flag");
```

Ruby seems more complicated at first sight, because it’s harder to only comment out either one of Ruby and Python. But remember that Python has docstring `"""..."""`, whereas Ruby has syntax like `""""` that evaluates to a single `""`. Leveraging this, we can comment out Ruby code in Python program. Oh, also remember that `__END__` terminates Ruby interpretation. This syntax comes handy because later on we don’t need to care about Ruby anymore. After some more tinkering, we get a program like this:

```ruby
#if 0
""""
print `cat flag`
__END__
"""
import os
p = os.system
#endif
#define p(s) main(){system(s);}
p("cat flag");
```

The hardest part is adding support for Haskell. Haskell has a rigid syntax that makes it hard to construct our polyglot. Intuition tells us that code in all other languages should be wrapped into a Haskell block comment like this:

```haskell
{-
...
-}main = do x <- readFile "flag"; putStr x
```

Unfortunately that won’t work because it is illegal in all other languages. To make it play nice with C, we can write something like `x = {-0}; //-}` and despite `gcc`’s warning it is an array literal. To make it a legal Python program we further extend it to be `x = {-0}; ... #define x //-}`, and it is interpreted as a set literal in Python. Ruby does not have set literal, but it has hash syntax `{key => value}`. Since all other languages does not recognize hash rocket token `=>`, we use the old Python docstring trick to make the program roughly look like: `x = {-0 + """".to_i => 0} ... __END__ """.find('x')} ... #define x //-} ...`. Finally we get a working polyglot that looks like this:

```
x = {-
#if 0
0 + """".to_i => 0}
print `cat flag`
__END__
""".find('x')}
import os
p = os.system;{
#endif
1};
#define p(s) main(){system(s);}
p("cat flag");
#define x // -}();main = do x <- readFile "flag"; putStr x
```

Showing the same code with syntax highlighting for each programming language clearly shows what gets executed:

**Python:**

```python
x = {-
#if 0
0 + """".to_i => 0}
print `cat flag`
__END__
""".find('x')}
import os
p = os.system;{
#endif
1};
#define p(s) main(){system(s);}
p("cat flag");
#define x // -}();main = do x <- readFile "flag"; putStr x
```

**Ruby:**

```ruby
x = {-
#if 0
0 + """".to_i => 0}
print `cat flag`
__END__
""".find('x')}
import os
p = os.system;{
#endif
1};
#define p(s) main(){system(s);}
p("cat flag");
#define x // -}();main = do x <- readFile "flag"; putStr x
```

**C:**

```c
x = {-
#if 0
0 + """".to_i => 0}
print `cat flag`
__END__
""".find('x')}
import os
p = os.system;{
#endif
1};
#define p(s) main(){system(s);}
p("cat flag");
#define x // -}();main = do x <- readFile "flag"; putStr x
```

**Haskell:**

```haskell
x = {-
#if 0
0 + """".to_i => 0}
print `cat flag`
__END__
""".find('x')}
import os
p = os.system;{
#endif
1};
#define p(s) main(){system(s);}
p("cat flag");
#define x // -}();main = do x <- readFile "flag"; putStr x
```

## Other write-ups and resources

* <http://tasteless.eu/2014/08/hitcon2014-polyglot-crazy500/>
* <http://www.hxp.io/blog/7/HITCON+CTF+2014%3A+crazy500+%22polyglot%22>
* <http://v0ids3curity.blogspot.in/2014/08/hitcon-ctf-2014-polyglot-crazy-500.html>
* <https://rzhou.org/~ricky/hitcon2014/polyglot/>
