# ASIS Cyber Security Contest Finals 2014: Satellite

**Category:** PPC
**Points:** 200
**Description:**

> Connect here and find the flag:
>
> ```bash
> nc asis-ctf.ir 12435
> ```

## Write-up

On connecting to the server, we get the following message:

```
hi all,  You must send a string for each level that would make the literal True
send "Sattelite"
```

When we sent `Sattelite` (sic), the server responded with [a SAT formula](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem), such as:

```
(x4 ∨ x5) ∧ (¬x3 ∨ ¬x1) ∧ (¬x3 ∨ x5) ∧ (x3 ∨ ¬x4) ∧ (x1 ∨ ¬x5)
```

That’s easy! Or at least it’s easy when you know logic and SAT. There are many SAT solvers, so just picking one of them and feeding them the formula should work. We chose `picosat`, because it has Python bindings through `pycosat`.

After transforming the input format into a format that `picosat` can read, we got a valid solution. On IRC we found out the format of the solution should be `11001` for the result `x1 ∧ x2 ∧ ¬x3 ∧ ¬x4 ∧ x5`. That’s also easy to transform, given the solution.

The only problem left is that sometimes, not all variables are used in the clauses (such as in our case the variable `x2`). We need to do a manual adjustment for that… First of all, if a missing variable has a lower number then the largest variable, this is not a problem, as `picosat` can solve that for itself. If a missing variable is larger then the largest variable, we need to append the result with some more ones or zeroes.

Using [the `solve.py` script](solve.py), we solve all the SAT formulas and get the flag `ASIS\_5b5e15ec25479ac8b743c6e818d75464`.

## Other write-ups and resources

* <http://tasteless.eu/2014/10/asis-ctf-finals-2014-sattelite-ppc-200/>
* <https://ctfcrew.org/writeup/81>
* <http://bruce30262.logdown.com/posts/237394-asis-ctf-finals-2014-satellite>
