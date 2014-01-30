# Exceptions
class StripeError(Exception):
    pass

class HTTPConnectionError(StripeError):
    pass
