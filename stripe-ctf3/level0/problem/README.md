# Level 0

## Usage

To submit your code, first commit, and then run `git push`.

Only the program input will vary; we'll always run against the same
dictionary (`test/harness` will download that dictionary for you if
you don't have it).

See https://stripe-ctf.com for context on this level.

## Observations

It's hard to know what this script does, but it seems to take time
depending on the size of the input:

    $ time ./level0 < short.txt >/dev/null

    real  0m1.231s
    user  0m1.132s
    sys   0m0.096s

Compare to:

    $ time ./level0 < long.txt >/dev/null

    real  0m14.060s
    user  0m12.952s
    sys   0m1.104s

`wc -c` shows that long.txt is about 10 times larger than short.txt,
so it seems like the runtime grows linearly with input size. Since it
also has to read the entire input, there's not going to be a way to do
better than a linear-time solution.

## Catalog

- `build.sh`: We'll run this file before trying to run your code. This
  is likely only relevant if you rewrite in another language, but it
  also could be useful for something like fetching dependencies via
  Bundler. Feel free to modify it arbitarily; we'll run the modified
  version on our build servers. (https://stripe-ctf.com/about#build
  has more information on the build process.)

- `level0`: The mysterious program. Why so slow?

- `long.txt`: An example long input file.

- `short.txt`: An example short input file.

- `README.md`: This file :).

- `test/*`: A framework to make it easy for you to run test cases
  locally. You should only ever have to run `test/harness`.
