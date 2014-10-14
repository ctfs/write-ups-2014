# 2014 Secuinside CTF Prequal: JavaScript jail

**Category:** Misc
**Points:** 200
**Description:**

> 54.178.218.50 6789

## Write-up

Provide replacement functions for `Math.random`, `Array.apply`, and `.map`
on the Array:

    Math.random = function(){return 1;};
    f = function(l) {
      print(l);
      var foo = Array(l);
      for (i=0;i<foo.length;i++) {
        foo[i] = Math.random() * 0x10000;
      }
      foo.map = function(){return foo};
      return foo;
    };
    Array.apply = function() { return f(30); };
    check(f);

## Other write-ups and resources

- [Matir's write-up](https://systemoverlord.com/blog/2014/06/02/secuinside-quals-2014-javascript-jail/)
- [Cugu's write-up](http://blog.cugu.eu/write-up-secuinside-ctf-2014-javascript-jail/)
