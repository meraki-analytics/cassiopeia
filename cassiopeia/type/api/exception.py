class CassiopeiaException(Exception):
    """Generic exception for a failure within Cassiopeia"""
    pass

class APIError(Exception):
    """Thrown when the RiotAPI returns an HTTP error code from a call"""
    def __init__(self, message, error_code):
        """
        message       str    the error message
        error_code    int    the HTTP error code that was received
        """
        super().__init__(message)
        self.error_code = error_code