try:
    from future.builtins.misc import super
except ImportError:
    pass


class CassiopeiaException(Exception):
    """Generic exception for a failure within Cassiopeia"""
    pass


class APIError(Exception):
    """"
    message       str    the error message
    error_code    int    the HTTP error code that was received
    """
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
