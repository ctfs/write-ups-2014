# Level 2

## Getting started

As in Level 0, you can run this level using `test/harness` and you can it
submit for scoring using `git push`. Your goal is to modify the
reverse proxy in `shield` to create a defensive proxy that mitigates
floods of malicious traffic. When you submit your `shield` for
scoring, we will run it using a copy of the network simulation code
that is available in `network_simulation/`.

To run the provide code, you will need a Node.js installation. See:

  http://nodejs.org

## Building

The provided `./build.sh` will install the level's Node.js
dependencies using the Node Package Manager (`npm`). Remember that
this build script will be run on our scoring servers to build your
submitted code, and you can modify it however you want.

## Included files

* `./shield` and `./build.sh`: You should modify these!
* `./network_simulation/`: a copy of the simulation code that we run on
  our servers. They are provided for your reference and for local
  simulations. We maintain our own copies of them for purposes of
  scoring.
** `backend.js`: the code for the fragile backend servers
** `sword.js` the code that simulates the malicious and legitimate
  traffic against the backends
* `./network_simulation/lib/`: some Node.js modules that are shared by the rest of the
  included code. Yours to modify (although you often won't need to).

## The simulation and scoring

### The layout of the simulated network

The network has three components: your proxy (`shield`), backends, and
clients. The standard configuration, used for scoring and used by
`test/harness`, is to have a backend listen on port 3001 and a second
on 3002. Then `shield` connects to the two backends and listens on
port `3000`. Then `sword.js` is run, and it simulates a swarm of many
clients (some legitimate and some malicious) connecting to the proxy.
Although there are two backends in the scoring simulation, the stub
code in `shield` does not perform any load balancing unless you modify
it to do so.

Technical note: the simulation framework uses HEAD requests to check
the upness of the `shield` and backends (it won't run until they're
up). If you are doing a major re-write, you should preserve the
current semantics around HEAD (see the `sword.js` source for more).

## The scoring

In the simulated environment, there are a large number of legitimate
clients making just a few requests each. There are also a small
number of malicious clients making an enormous number of requests
each. Think of these as mice and elephants: the goal of the level is
to let the mice through while keeping the elephants out.

The scoring simulation runs for 20 seconds. During that period, you
receive one point each time that you successfully proxy a response to
a request that was made by a mouse. At the end of the 20 seconds, you
lose points in proportion to the idleness of your backend boxes
(i.e. if you don't have an opportunity to proxy a mouse request, it is
better to proxy an elephant request than do nothing).

When the requests are coming in they are not labeled as
legitimate or malicious. However, the originating IP is
identified by the 'X-Forwarded-For' header on each packet. You can
determine, by watching the network whether an IP is malicious. A
given IP is either always malicious or always legitimate


