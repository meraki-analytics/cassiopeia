class CassiopeiaException(Exception):
    pass

class APIError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code