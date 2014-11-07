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
            listing = listdir(directory)
            listing = [e for e in listing if not e.startswith('.')]
            return listing
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
        return "NCN" + sha1("This is the New World Order").hexdigest()

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
