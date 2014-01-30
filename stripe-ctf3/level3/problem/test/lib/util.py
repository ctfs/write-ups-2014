import logging
import os
from random import SystemRandom
import sys

logger = logging.getLogger('stripe')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

__all__ = ['StringIO', 'json', 'utf8', 'random_letters', 'mkdir_p']

if sys.version_info < (3,0):
    # Used to interface with pycurl, which we only make available for
    # those Python versions
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO

try:
    import json
except ImportError:
    json = None

if not (json and hasattr(json, 'loads')):
    try:
        import simplejson as json
    except ImportError:
        if not json:
            raise ImportError(
                "Stripe requires a JSON library, such as simplejson. "
                "HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' or "
                "'easy_install simplejson'.")
        else:
            raise ImportError(
                "Stripe requires a JSON library with the same interface as "
                "the Python 2.6 'json' library.  You appear to have a 'json' "
                "library with a different interface.  Please install "
                "the simplejson library.  HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' "
                "or 'easy_install simplejson'.")


def utf8(value):
    if sys.version_info < (3, 0) and isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def random_letters(count=4):
    LETTERS = "abcdefghijklmnopqrstuvwxyz"
    output = []
    for i in range(0, count):
        output.append(SystemRandom().choice(LETTERS))
    return "".join(output)

# TODO: Python >2.5 ?
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.isdir(path): pass
        else: raise

def exception_as():
    _, err, _ = sys.exc_info()
    return err
