r"""Class to send and receive raw data.

Example:

>>> from netcatlib import *
>>> nc = Netcat('127.0.0.1', 8080)
>>> nc.read_until("your name is: ")
>>> addr_system = nc.read_format("<I") + 0x7Ce
>>> nc.write('My exploit: \x01\x02\x70\xff\xff\xbf/bin/sh -i\n')
>>> nc.interact()

We use EOFError to distinguish between "no data" and "connection
closed". Also note that the socket appears ready for reading when
it is actually closed.

To do:
- Windows: Improve exiting the stdin loop when the connection has been closed
    in the `interact` function.

"""

# Imported modules
import sys, socket, select, struct

__all__ = ["Netcat"]

# Tunable parameters
DEBUGLEVEL = 0

class Netcat:

    """Netcat interface class.

    An instance of this class represents a connection to a tcp endpoint.
    The instance is initially not connected; the open() method must be
    used to establish a connection.  Alternatively, the host name and
    optional port number can be passed to the constructor, too.

    Don't try to reopen an already connected instance.

    This class has many read_*() methods.  Note that some of them
    raise EOFError when the connection is closed, while others return
    the empty string ''. See the individual doc strings for details.

    read_until(expected, [timeout])
        Read until the expected string has been seen, or a timeout is
        hit (default is no timeout); may block.

    read_exact(amount)
        Read exactly amount number of bytes.

    read_format(format)
        Read and unpack data according to the supplied format.

    read_eager()
        Read everything that's possible without blocking in I/O.

    read_buffered()
        Reads all data in the buffered queue, without doing any socket I/O.

    read_all()
        Read all data until EOF; may block.

    read_some()
        Read at least one byte or EOF; may block.
		
    expect(list, [timeout]):
        Read until one from a list of a regular expressions matches, or
        a timeout is hit (default is no timeout).

    """

    def __init__(self, host=None, port=80,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance; port number
        and timeout are optional.
        """
        self.debuglevel = DEBUGLEVEL
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.buffer = ''       # buffered queue
        self.eof = 0
        if host is not None:
            self.open(host, port, timeout)

    def open(self, host, port, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host.

        Don't try to reopen an already connected instance.
        """
        self.eof = 0
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        """Destructor -- close the connection."""
        self.close()

    def msg(self, msg, *args):
        """Print a debug message, when the debug level is > 0.

        If extra arguments are present, they are substituted in the
        message using the standard string formatting operator.

        """
        if self.debuglevel > 0:
            print 'Netcat(%s,%d):' % (self.host, self.port),
            if args:
                print msg % args
            else:
                print msg

    def set_debuglevel(self, debuglevel):
        """Set the debug level.

        The higher it is, the more debug output you get (on sys.stdout).

        """
        self.debuglevel = debuglevel

    def close(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
        self.sock = 0
        self.eof = 1

    def get_socket(self):
        """Return the socket object used internally."""
        return self.sock

    def fileno(self):
        """Return the fileno() of the socket object used internally."""
        return self.sock.fileno()

    def write(self, buffer):
        """Write a string to the socket.

        Can block if the connection is blocked.  May raise
        socket.error if the connection is closed.

        """
        self.msg("send %r", buffer)
        self.sock.sendall(buffer)

    def read_until(self, match, timeout=None):
        """Read until a given string is encountered or until timeout.

        When no match is found, return whatever is available instead,
        possibly the empty string.  Raise EOFError if the connection
        is closed and no buffered data is available.

        """
        n = len(match)
        self.recv_blocking()
        i = self.buffer.find(match)
        if i >= 0:
            i = i+n
            buf = self.buffer[:i]
            self.buffer = self.buffer[i:]
            return buf
        s_reply = ([self], [], [])
        s_args = s_reply
        if timeout is not None:
            s_args = s_args + (timeout,)
            from time import time
            time_start = time()
        while not self.eof and select.select(*s_args) == s_reply:
            i = max(0, len(self.buffer)-n)
            self.recv_blocking()
            i = self.buffer.find(match, i)
            if i >= 0:
                i = i+n
                buf = self.buffer[:i]
                self.buffer = self.buffer[i:]
                return buf
            if timeout is not None:
                elapsed = time() - time_start
                if elapsed >= timeout:
                    break
                s_args = s_reply + (timeout-elapsed,)
        return self.read_buffered()

    def read_exact(self, amount=1):
        """Read at exactly amount bytes of data unless EOF is hit.

        Blocks if insufficient data is available to fulfill the request.
        Raises EOFError if connection is closed before sufficient data
        has been received.

        """
        #while not self.buffer and len(self.buffer) < amount and not self.eof:
        while len(self.buffer) < amount and not self.eof:
            self.recv_blocking()

        if len(self.buffer) < amount:
            raise EOFError

        buf = self.buffer[:amount]
        self.buffer = self.buffer[amount:]
        return buf

    def read_format(self, format):
        """Read the struct specified by format.

        Blocks if insufficient data is available to unpack the struct.
        A struct of one element is automatically unpacked."""
        length = struct.calcsize(format)
        data = struct.unpack(format, self.read_exact(length))
        return data[0] if len(data) == 1 else data

    def read_eager(self):
        """Read everything that's possible without blocking in I/O (eager).

        Raise EOFError if connection closed and no buffered data
        available.  Return '' if no buffered data available otherwise.

        """
        while not self.buffer and not self.eof and self.sock_avail():
            self.recv_blocking()
        return self.read_buffered()

    def read_buffered(self):
        """Return any data available in the buffered queue (very lazy).

        Raise EOFError if connection closed and no data available.
        Return '' if no buffered data available otherwise.  Don't block.

        """
        buf = self.buffer
        self.buffer = ''
        if not buf and self.eof:
            raise EOFError
        return buf

    def read_all(self):
        """Read all data until EOF; block until connection closed."""
        while not self.eof:
            self.recv_blocking()
        buf = self.buffer
        self.buffer = ''
        return buf

    def read_some(self, amount=1):
        """Read at least one byte of buffered data unless EOF is hit.

        Return '' if EOF is hit.  Block if no data is immediately
        available.

        """
        while not self.buffer and len(self.buffer) < amount and not self.eof:
            self.recv_blocking()
        buf = self.buffer
        self.buffer = ''
        return buf

    def recv_blocking(self):
        """Transfer from raw queue to buffered queue.

        Set self.eof when connection is closed. Blocks if no input
        is available. Raise EOFError when connection is closed.

        """

        # Get data in the raw queue
        buf = self.sock.recv(1024)
        self.msg("recv %r", buf)
        self.eof = (not buf)
        self.buffer += buf

    def sock_avail(self):
        """Test whether data is available on the socket."""
        return select.select([self], [], [], 0) == ([self], [], [])

    def interact(self):
        """Show output to screen, and let user send input."""
        sys.stdout.write(self.read_buffered())
        sys.stdout.flush()

        if sys.platform == "win32":
            mt_interact_exit = False
            self.mt_interact()
            return
        while 1:
            rfd, wfd, xfd = select.select([self, sys.stdin], [], [])
            if self in rfd:
                try:
                    text = self.read_eager()
                except EOFError:
                    print '*** Connection closed by remote host ***'
                    break
                if text:
                    sys.stdout.write(text)
                    sys.stdout.flush()
            if sys.stdin in rfd:
                line = sys.stdin.readline()
                if not line:
                    break
                self.write(line)

    def mt_interact(self):
        """Multithreaded version of interact()."""
        global mt_interact_exit
        import thread

        mt_interact_exit = False
        threadid = thread.start_new_thread(self.listener, ())
        while 1:
            line = sys.stdin.readline()
            if not line or mt_interact_exit:
                break
            self.write(line)

    def listener(self):
        global mt_interact_exit
        """Helper for mt_interact() -- this executes in the other thread."""
        while 1:
            select.select([self], [], [])
            try:
                data = self.read_eager()
            except EOFError:
                mt_interact_exit = True
                print '*** Connection closed by remote host ***'
                print 'Press enter to close interaction...',
                return
            if data:
                sys.stdout.write(data)
            else:
                sys.stdout.flush()

    def expect(self, list, timeout=None):
        """Read until one from a list of a regular expressions matches.

        The first argument is a list of regular expressions, either
        compiled (re.RegexObject instances) or uncompiled (strings).
        The optional second argument is a timeout, in seconds; default
        is no timeout.

        Return a tuple of three items: the index in the list of the
        first regular expression that matches; the match object
        returned; and the text read up till and including the match.

        If EOF is read and no text was read, raise EOFError.
        Otherwise, when nothing matches, return (-1, None, text) where
        text is the text received so far (may be the empty string if a
        timeout happened).

        If a regular expression ends with a greedy match (e.g. '.*')
        or if more than one expression can match the same input, the
        results are undeterministic, and may depend on the I/O timing.

        """
        re = None
        list = list[:]
        indices = range(len(list))
        for i in indices:
            if not hasattr(list[i], "search"):
                if not re: import re
                list[i] = re.compile(list[i])
        if timeout is not None:
            from time import time
            time_start = time()
        while 1:
            for i in indices:
                m = list[i].search(self.buffer)
                if m:
                    e = m.end()
                    text = self.buffer[:e]
                    self.buffer = self.buffer[e:]
                    return (i, m, text)
            if self.eof:
                break
            if timeout is not None:
                elapsed = time() - time_start
                if elapsed >= timeout:
                    break
                s_args = ([self.fileno()], [], [], timeout-elapsed)
                r, w, x = select.select(*s_args)
                if not r:
                    break
            self.recv_blocking()
        text = self.read_buffered()
        if not text and self.eof:
            raise EOFError
        return (-1, None, text)


def test():
    """Test our library"""

    nc = Netcat("www.google.com", 80)
    nc.write("GET / HTTP/1.1\n\rHost: www.google.com\n\r\n\r")
    print "Untill:", nc.read_until("Control: ")
    print "Buffered:", nc.read_buffered()
    nc.interact()

if __name__ == '__main__':
    test()
