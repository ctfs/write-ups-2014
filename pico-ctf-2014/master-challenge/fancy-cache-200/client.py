#!/usr/bin/python
import struct
import socket
import telnetlib

def pack4(v):
    """
    Takes a 32 bit integer and returns a 4 byte string representing the
    number in little endian.
    """
    assert 0 <= v <= 0xffffffff
    # The < is for little endian, the I is for a 4 byte unsigned int.
    # See https://docs.python.org/2/library/struct.html for more info.
    return struct.pack('<I', v)

def unpack4(v):
    """Does the opposite of pack4."""
    assert len(v) == 4
    return struct.unpack('<I', v)[0]

CACHE_GET = 0
CACHE_SET = 1

kNotFound = 0x0
kFound = 0x1
kCacheFull = 0x2

def write_string(f, s):
    f.write(pack4(len(s)))
    f.write(s)

def read_string(f):
    size = unpack4(f.read(4))
    return f.read(size)

def cache_get(f, key):
    f.write(chr(CACHE_GET))
    write_string(f, key)

    status = ord(f.read(1))
    if status == kNotFound:
        return None
    assert status == kFound

    return read_string(f)

def cache_set(f, key, value, lifetime):
    f.write(chr(CACHE_SET))
    write_string(f, key)

    status = ord(f.read(1))
    if status == kCacheFull:
        return False
    assert status == kFound

    write_string(f, value)
    f.write(pack4(lifetime))
    return True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1337))
f = s.makefile('rw', bufsize=0)

# It's useful to pause the client right after connecting so that you can
# attach to the server with gdb if desired.
raw_input()

# Add an entry to the cache
assert cache_set(f, 'cache key', 'cache value', 1024)

# Retrieve it back
assert cache_get(f, 'cache key') == 'cache value'

# Once you get the service to run a shell, this lets you send commands
# to the shell and get the results back :-)
'''
t = telnetlib.Telnet()
t.sock = s
t.interact()
'''
