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

We starts from Python2/3:

```python
import os
os.system("cat flag");
```

To make gcc happy, we need some polyglot syntax to comment out import statement in C. Recall that C has compiler directives that starts with `#`, which is also line comment in Python. Conditional compilation seems to be a ideal choice because it also acts as block comment in C. Then we can define a macro for `main` so that both Python and C looks good.

```c
#if 0
import os
p = os.system
#endif
#define p(s) main(){system(s);}
p("cat flag");
```

Ruby seems more complicated at first sight, because it's harder to only comment out either one of Ruby and Python. But remember that Python has docstring `"""..."""`, whereas Ruby has syntax like `""""` that evaluates to a single `""`. Leveraging this, we can comment out Ruby code in Python program. Oh, also remember that `__END__` terminates Ruby interpretation. This syntax comes handy becaues later on we don't need to care about Ruby anymore. After several attempts, we got a program like this:

```ruby
#if 0
""""
print `cat flag`
__END__
"""
#endif
import os
p = os.system
#define p(s) main(){system(s);}
p("cat flag");
```

The hardest part comes when we are trying to have Haskell. Haskell has a rigid syntax that makes it hard to construct our polyglot. Intuition tells us that code if all other languages should be wrapped into a Haskell block comment like this:

```haskell
{-
...
-}main = do x <- readFile "flag"; putStr x
```

Unfortunately it won't work because it is illegal in all other languages. To make it play nice with C, we can write something like `x = {-0}; //-}` and despite gcc's warning it is an array literal. To make it a legal Python program we further extend it to be `x = {-0}; #define x //-}`, and it is interpreted as a set literal in Python. Ruby does not have set literal, but it has hash syntax `{key => value}`. Since all other languages does not recognize hash rocket token `=>`, we use the old Python docstring trick to make the program roughly looks like: `x = {-0 + """".to_i => 0} ... __END__ """.find('x')} ... #define x //-} ...`. After a few tries, we finally got a working polyglot that looks like this:

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

## Other write-ups

* <http://tasteless.se/2014/08/hitcon2014-polyglot-crazy500/>
