import os
import sys
import textwrap

# From this package
import lib.error as error
import lib.util as util

# This is a port of http_client from [Stripe-Python](https://github.com/stripe/stripe-python)

# - Requests is the preferred HTTP library
# - Use Pycurl if it's there (at least it verifies SSL certs)
# - Fall back to urllib2 with a warning if needed

try:
    if sys.version_info < (3,0):
        import urllib2 as urllib_request
    else:
        import urllib.request as urllib_request
except ImportError:
    pass

try:
    import pycurl
except ImportError:
    pycurl = None

try:
    import requests
except ImportError:
    requests = None
else:
    try:
        # Require version 0.8.8, but don't want to depend on distutils
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split('.')]
    except Exception:
        # Probably some new-fangled version, so it should support verify
        pass
    else:
        if (major, minor, patch) < (0, 8, 8):
            util.logger.warn(
                'Warning: the test harness will only use your Python "requests"'
                'library if it is version 0.8.8 or newer, but your '
                '"requests" library is version %s. We will fall back to '
                'an alternate HTTP library so everything should work. We '
                'recommend upgrading your "requests" library. (HINT: running '
                '"pip install -U requests" should upgrade your requests '
                'library to the latest version.)' % (version,))
            requests = None

def certs_path():
    return os.path.join(os.path.dirname(__file__), 'ca-certificates.crt')


def new_default_http_client(*args, **kwargs):
    if requests:
        impl = RequestsClient
    elif pycurl and sys.version_info < (3,0):
        # Officially supports in 3.1-3.3 but not 3.0. The idea is that for >=2.6
        # you should use requests
        impl = PycurlClient
    else:
        impl = Urllib2Client
        if sys.version_info < (2,6):
            reccomendation = "pycurl"
        else:
            reccomendation = "requests"
        util.logger.info(
            "Warning: The test harness is falling back to *urllib2*. "
            "Its SSL implementation doesn't verify server "
            "certificates (how's that for a distributed systems problem?). "
            "We recommend instead installing %(rec)s via `pip install %(rec)s`.",
            {'rec': reccomendation})

    return impl(*args, **kwargs)


class HTTPClient(object):

    def __init__(self, headers={}, verify_ssl_certs=True):
        self._verify_ssl_certs = verify_ssl_certs
        self.headers = headers

    def request(self, method, url, post_data=None):
        raise NotImplementedError(
            'HTTPClient subclasses must implement `request`')


class RequestsClient(HTTPClient):
    name = 'requests'

    def request(self, method, url, post_data=None):
        kwargs = {}

        if self._verify_ssl_certs:
            kwargs['verify'] = certs_path()
        else:
            kwargs['verify'] = False

        try:
            try:
                result = requests.request(method,
                                          url,
                                          headers=self.headers,
                                          data=post_data,
                                          timeout=80,
                                          **kwargs)
            except TypeError:
                e = util.exception_as()
                raise TypeError(
                    'Warning: It looks like your installed version of the '
                    '"requests" library is not compatible with Stripe\'s '
                    'usage thereof. (HINT: The most likely cause is that '
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    'underlying error was: %s' % (e,))

            # This causes the content to actually be read, which could cause
            # e.g. a socket timeout. TODO: The other fetch methods probably
            # are succeptible to the same and should be updated.
            content = result.content
            status_code = result.status_code
        except Exception:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            e = util.exception_as()
            self._handle_request_error(e)
        if sys.version_info >= (3, 0):
            content = content.decode('utf-8')
        return content, status_code

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
        msg = "Network error: %s" % (err,)
        raise error.HTTPConnectionError(msg)

class PycurlClient(HTTPClient):
    name = 'pycurl'

    def request(self, method, url, post_data=None):
        s = util.StringIO.StringIO()
        curl = pycurl.Curl()

        if method == 'get':
            curl.setopt(pycurl.HTTPGET, 1)
        elif method == 'post':
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDS, post_data)
        else:
            curl.setopt(pycurl.CUSTOMREQUEST, method.upper())

        # pycurl doesn't like unicode URLs
        curl.setopt(pycurl.URL, util.utf8(url))

        curl.setopt(pycurl.WRITEFUNCTION, s.write)
        curl.setopt(pycurl.NOSIGNAL, 1)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 80)
        curl.setopt(pycurl.HTTPHEADER, ['%s: %s' % (k, v)
                    for k, v in self.headers.iteritems()])
        if self._verify_ssl_certs:
            curl.setopt(pycurl.CAINFO, certs_path())
        else:
            curl.setopt(pycurl.SSL_VERIFYHOST, False)

        try:
            curl.perform()
        except pycurl.error:
            e = util.exception_as()
            self._handle_request_error(e)
        rbody = s.getvalue()
        rcode = curl.getinfo(pycurl.RESPONSE_CODE)
        return rbody, rcode

    def _handle_request_error(self, e):
        error_code = e[0]
        if error_code in [pycurl.E_COULDNT_CONNECT,
                          pycurl.E_COULDNT_RESOLVE_HOST,
                          pycurl.E_OPERATION_TIMEOUTED]:
            msg = ("Test harness could not connect to Stripe. Please check "
                   "your internet connection and try again.")
        elif (error_code in [pycurl.E_SSL_CACERT,
                             pycurl.E_SSL_PEER_CERTIFICATE]):
            msg = "Could not verify host's SSL certificate."
        else:
            msg = ""
        msg = textwrap.fill(msg) + "\n\nNetwork error: %s" % e[1]
        raise error.HTTPConnectionError(msg)


class Urllib2Client(HTTPClient):
    if sys.version_info >= (3, 0):
        name = 'urllib.request'
    else:
        name = 'urllib2'

    def request(self, method, url, post_data=None):
        if sys.version_info >= (3, 0) and isinstance(post_data, str):
            post_data = post_data.encode('utf-8')

        req = urllib_request.Request(url, post_data, self.headers)

        if method not in ('get', 'post'):
            req.get_method = lambda: method.upper()

        try:
            response = urllib_request.urlopen(req)
            rbody = response.read()
            rcode = response.code
        except urllib_request.HTTPError:
            e = util.exception_as()
            rcode = e.code
            rbody = e.read()
        except (urllib_request.URLError, ValueError):
            e = util.exception_as()
            self._handle_request_error(e)
        if sys.version_info >= (3, 0):
            rbody = rbody.decode('utf-8')
        return rbody, rcode

    def _handle_request_error(self, e):
        msg = "Network error: %s" % str(e)
        raise error.HTTPConnectionError(msg)
