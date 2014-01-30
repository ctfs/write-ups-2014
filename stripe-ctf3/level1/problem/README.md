# Gitcoin

Welcome to the wonderful world of Gitcoin!

## Overview

The balances are all contained in `LEDGER.txt`. We also have provided
you with a sample Gitcoin mining script in `miner` -- you'll probably
notice it's too slow to use in practice though. Note that for this
level you won't submit any code to us, as you'll be running everything
locally (you're welcome to email us solutions if you think they are
particularly cool, though).

The only commits that can be pushed are ones that:

- Increments an existing ledger entry by 1, or adds a new ledger entry
  with balance: 1; and
- Has a SHA1 lexicographically less than the value in `difficulty.txt`.

Add yourself to `LEDGER.txt` to pass the level (worth 50 points), at
which points the bots will stop.

Once you're done, check your account page to advance to the global
Gitcoin instance, where you can earn unbounded numbers of leaderboard
points.

Note that until you pass the level we'll periodically start a new
Gitcoin instance, at which point you'll have to run `git reset --hard
origin/master` to reset your clone's state.

## Catalog

- `difficulty.txt`: A strict upper bound on valid Gitcoin SHA1 values.

- `miner`: A sample Gitcoin mining script.

- `LEDGER.txt`: The current Gitcoin balances.

- `README.md`: This file.
