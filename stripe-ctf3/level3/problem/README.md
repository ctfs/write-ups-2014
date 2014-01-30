# Level 3

## API

Instant Code Search defines the following HTTP endpoints. All of them
return JSON.

- /healthcheck:
Returns '{"success": "true"}' if all the nodes are up and ready to receive
requests.

- /index?path=PATH:
Takes a path on the filesystem and indexes it.

- /isIndexed:
Returns '{"success": "true"}' if all the nodes have indexed paths, and are
ready to receive queries.

- /?q=QUERY
Returns any file and line number in the indexed path. The response is of
this form:

    {
      "success": true,
      "results": [
        "path/to/file1:5",
        "path/to/another/file:33",
        ...
      ]
    }

All of these endpoints have been implemented, but we could use your expertise
in making the query endpoint a _lot_ faster.

## Usage

To start a specific server, run `bin/start-server`. This looks to see if
your jar is assembled; if it is, it runs the jar, and if not, uses sbt[1].

To start all of your nodes, run `bin/start-servers`. This will start a
master search node, and three search nodes. The master node is the only
node that we communicate with.

The master node runs on port 9090 (and the search nodes on 9091, 9092, and
9093). Once the servers are up, you can point your browser at
http://localhost:9090 to communicate with (and query) the master node.

As always, to submit your code, first commit, and then run `git push`.

You can test your code locally via `test/harness`[2]. You can use the
harness to download the test cases we run your code against.

Note that the input is generated randomly on a seed; we'll always run
against the same dictionary (the harness will download that dictionary for
you if you don't have it).

## Constraints

We're limiting the amount of memory that each of your nodes gets to 500mb.

When running your solution, we'll give you up to 4 minutes to index,
after which, ready or not, we'll start sending queries your way!

(We'll be polling `/isIndexed` in the meanwhile, and if at any point, you're
ready to start accepting queries, we'll start sending them.)

## Scoring

The scoring in this level is based on a single metric: the average request
latency over 50 requests. Your score is a function of the ratio of your
average response time to the default solution.

To beat the level, you will have to perform 4 times as fast as the default
solution in this repository.

Good luck!

[1] Scala Build Tool: http://www.scala-sbt.org/
