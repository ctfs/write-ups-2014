# Plaid CTF 2014: g++

**Category:** Reversing
**Points:** 200
**Description:**

> Although it seems like The Plague's projects are open source, it's not quite so simple to figure out what the source code does. We believe [this project](g++-30f6a74ce24ea3605ba7cbec92222a72.tar.bz2) is supposed to print out secret information, but the KEY variable in the Makefile has been lost. Find the key, build the project, get us the information.

## Write-up

_This write-up is made by Xor0X of [HacknamStyle](http://hacknamstyle.net/)._

In the `Makefile` a key can be configured. Using a simple script the key is converted to the header file `key.h`. The character at index `i` with ASCII value `v` is encoded as `K(i, v)`. So the password `test` becomes:

```
K(0,116) // 't'
K(1,101) // 'e'
K(2,115) // 's'
K(3,116) // 't'
```

In `solveme.cpp` this key is then stored using template specialization:

```cpp
template <int i> struct key { S r = 0; };
#define K(i,v) template<> struct key<i> { S r = v; };
```

Hence using `key<i>::r` will return the key at position `i` (or `0` when the index is out of range). The code in `solveme.cpp` continues to use C++ [template metaprogramming](https://en.wikipedia.org/wiki/Template_metaprogramming) to verify this password at compile time. At runtime it checks the result of the compile time operation, and says if they key was correct or not:

```cpp
int main() {
  if (!vv<0>::r)
    // print 16 characters (aka the key)
  else
    std::cout << "Wrong\n";
  return 0;
}
```

From this we can tell the key is 16 characters long. Now we have to reverse engineer all the `#define`s and templates. This can be done by slowly refactoring them. This is tedious work, and we want to be sure our modifications are correct. The first option is to print out the result of `vv<0>::r` and assure our changes do not modify it. We can do better though. Take a look at how `vv<0>::r` is calculated:

```cpp
template <int n> struct vvv { S r = gg<n>::r|gg<n+1>::r|gg<n+2>::r|gg<n+3>::r; };
template <int n> struct vv { S r = vvv<0>::r|vvv<4>::r|vvv<8>::r|vvv<12>::r; };
```

We learn that the value `vv<0>::r` is based on the values `gg<i>::r` with `i` ranging between `0` and `15`. So we can print all the `gg<i>::r` values and assure they never change when we refactor the code. Remark that `vv<0>::r` is zero (and the password is correct) if and only if all the `gg<i>::r` are zero.

### Reversing Results

Reversing the `#define`s is left as an exercise for the reader (they are boring to read about anyway). In the end the definition of `gg` becomes:

```cpp
// 0 <= n <= 15
template <int n> struct gg {
  static const int r = (((hiddenkey<n,n|2>::r)) % 257) - makefilekey<(n>>2),((n)&3)>::rr;
};
```

We can see that both operands of the subtraction must be zero for the key to be valid. Furthermore, `makefilekey` depends on the key supplied in the `Makefile`, while `hiddenkey` only depends on data present in `solveme.cpp`. We don’t need to know how `hiddenkey` is calculated, we simply extract the values for all `n`. Now we want to find a key so that `gg<i>::r` is zero for all `i`. This means `makefilekey<(n>>2),((n)&3)>` must match `hiddenkey<n,n|2>::r` for `n` between `0` and `15`. So how is `makefilekey<a,b>::r` computed?

```cpp
template <int a, int b> struct makefilekey
{
  static const int rr = (lookup<(a)*4>::r * key<b>::r
                      + lookup<(a)*4+1>::r * key<b+4>::r
                      + lookup<(a)*4+2>::r * key<b+8>::r
                      + lookup<(a)*4+3>::r * key<b+12>::r) % 257;
};
```

Here `lookup` only depends on internal data in `solveme.cpp`. What’s crucial here is that `makefilekey<a,b>::r` only depends on four key bytes. In turn this means that `gg<0>::r`, `gg<4>::r`, `gg<8>::r`, and `gg<12>::r` depend only on `key<0>`, `key<4>`, `key<8>`, and `key<12>`. Hence these four key bytes can be bruteforced independently. The same is true for `key<1>`, `key<5>`, `key<9>`, and `key<13>`: They can also be bruteforced independent of the other bytes. In fact we can bruteforce the complete password in groups of four bytes. This is done by extracting the value of `lookup`, performing the calculation in `makefilekey`, and checking if they match the corresponding `hiddenkey` values.

My fully simplified solution can be found in [`solveme-simplified.cpp`](solveme-simplified.cpp).

### Solution

This solution bruteforces the keys in groups of four bytes:

```cpp
#include <stdio.h>

static const int hiddenkey_table[] = {
  15, 25, 172, 31, 100, 17, 225, 137,
  162, 71, 187, 191, 11, 105, 176, 94
};

static const int lookup_table[] = {
  13, 68, 87, 202, 29, 244, 71, 122,
  173, 228, 247, 42, 125, 148, 39, 90
};

static int calc_makefilekey(const char *password, int n) {
  int a = n / 4;
  int b = n % 4;

  return (lookup_table[a*4] * password[b] + lookup_table[a*4+1] * password[b+4]
    + lookup_table[a*4+2] * password[b+8] + lookup_table[a*4+3] * password[b+12]) % 257;
}

int main() {
  char crackedpw[20] = {0};

  // Crack key in groups of 4 chars at once
  for (int off = 0; off < 4; ++off) {
    bool found = false;
    printf("Cracking at offset %d...\n", off);

    for (int c1 = ' '; !found && c1 <= '~'; ++c1) {
      crackedpw[off] = c1;
      for (int c2 = ' '; !found && c2 <= '~'; ++c2) {
        crackedpw[off+4] = c2;
        for (int c3 = ' '; !found && c3 <= '~'; ++c3) {
          crackedpw[off+8] = c3;
          for (int c4 = ' '; !found && c4 <= '~'; ++c4) {
            crackedpw[off+12] = c4;

            if (
              calc_makefilekey(crackedpw, off) == hiddenkey_table[off]
              && calc_makefilekey(crackedpw, off+4) == hiddenkey_table[off+4]
              && calc_makefilekey(crackedpw, off+8) == hiddenkey_table[off+8]
              && calc_makefilekey(crackedpw, off+12) == hiddenkey_table[off+12]
            ) {
              found = true;
            }
          }
        }
      }
    }
  }

  printf("Cracked password: %s\n", crackedpw);
}
```

The solution is `C++_m0re_lyk_C--`.

### Comments

You can also solve this by constructing and solving the linear equations (with the key bytes as unknowns). For example, for the key bytes at position 0, 4, 8, and 12 we have the linear equations:

```
( 13 * k0 +  68 * k4 +  87 * k8 + 202 * k12) Mod 257 =  15
( 29 * k0 + 244 * k4 +  71 * k8 + 122 * k12) Mod 257 = 100
(173 * k0 + 228 * k4 + 247 * k8 +  42 * k12) Mod 257 = 162
(125 * k0 + 148 * k4 +  39 * k8 +  90 * k12) Mod 257 =  11
```

Using the `gaussJordan.py` file [found here](http://anh.cs.luc.edu/331/code/) we can solve this system using Python:

```python
>>> import guassJordan as gj
>>> A = [[13, 68, 87, 202, 15],
     [29, 244, 71, 122, 100],
     [173, 228, 247, 42, 162],
     [125, 148, 39, 90, 11]]
>>> t = gj.matConvert(A, gj.ZMod(257))
>>> gj.gauss_jordanExactField(t)
True
>>> t
[[Mod(1, 257), Mod(0, 257), Mod(0, 257), Mod(0, 257), Mod(67, 257)],
 [Mod(0, 257), Mod(1, 257), Mod(0, 257), Mod(0, 257), Mod(109, 257)],
 [Mod(0, 257), Mod(0, 257), Mod(1, 257), Mod(0, 257), Mod(95, 257)],
 [Mod(0, 257), Mod(0, 257), Mod(0, 257), Mod(1, 257), Mod(95, 257)]]
>>> chr(67), chr(109), chr(95), chr(95)
('C', 'm', '_', '_')
```

These characters match the solution of our bruteforce attack. Note that the Python files required to run this have been mirrored in the directory of this write-up.

## Other write-ups and resources

* <https://fail0verflow.com/blog/2014/plaidctf2014-re200-gxx.html>
* <https://docs.google.com/a/google.com/document/d/1jo_taidfAJsCbWUIpU9dYryhtTQr5YLON7BnIr0WN-k/edit>
* [Source code for this challenge, released after the CTF](https://github.com/pwning/plaidctf2014/tree/master/reversing/g%2B%2B)
* [Indonese](http://blog.rentjong.net/2014/04/plaidctf2014-write-up-g-reversing200.html)
* <http://j00ru.vexillium.org/dump/ctf/g++.cc>
