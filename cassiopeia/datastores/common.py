import re
import zlib
from contextlib import contextmanager
from io import BytesIO
from typing import Mapping, MutableMapping, Any, Union, Dict
from urllib.parse import urlencode

from pycurl import Curl
from merakicommons.ratelimits import RateLimiter

try:
    import certifi
except ImportError:
    certifi = None

try:
    import ujson as json
except ImportError:
    import json


_print_calls = True


class HTTPError(RuntimeError):
    def __init__(self, message, code, response_headers: Dict[str, str] = None):
        super().__init__(message)
        self.code = code
        self.response_headers = response_headers or {}


class HTTPClient(object):
    @staticmethod
    def _execute(curl: Curl, close_connection: bool) -> int:
        curl.perform()
        status_code = curl.getinfo(curl.HTTP_CODE)
        if close_connection:
            curl.close()
        return status_code

    @staticmethod
    def _get(url: str, headers: Mapping[str, str] = None, rate_limiter: RateLimiter = None, connection: Curl = None) -> (int, bytes, dict):
        if not headers:
            request_headers = ["Accept-Encoding: gzip"]
        else:
            request_headers = ["{header}: {value}".format(header=key, value=value) for key, value in headers.items()]
            if "Accept-Encoding" not in headers:
                request_headers.append("Accept-Encoding: gzip")

        response_headers = {}

        def get_response_headers(header_line: bytes) -> None:
            header_line = header_line.decode("ISO-8859-1")

            if ":" not in header_line:
                return

            name, value = header_line.split(":", 1)
            response_headers[name.strip()] = value.strip()

        buffer = BytesIO()

        curl = connection if connection is not None else Curl()

        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, buffer)
        curl.setopt(curl.HEADERFUNCTION, get_response_headers)
        curl.setopt(curl.HTTPHEADER, request_headers)
        if certifi:
            curl.setopt(curl.CAINFO, certifi.where())

        if _print_calls:  # TODO
            print("Making call: {}".format(url))
        if rate_limiter:
            with rate_limiter:
                status_code = HTTPClient._execute(curl, connection is None)
        else:
            status_code = HTTPClient._execute(curl, connection is None)

        body = buffer.getvalue()

        # Decompress if we got gzipped data
        try:
            content_encoding = response_headers["Content-Encoding"].upper()
            if "GZIP" == content_encoding:
                body = zlib.decompress(body, zlib.MAX_WBITS | 16)
        except KeyError:
            pass

        return status_code, body, response_headers

    def get(self, url: str, parameters: MutableMapping[str, Any] = None, headers: Mapping[str, str] = None, rate_limiter: RateLimiter = None, connection: Curl = None) -> (Union[dict, list, str, bytes], dict):
        if parameters:
            parameters = {k: str(v).lower() if isinstance(v, bool) else v for k, v in parameters.items()}
            parameters = urlencode(parameters, doseq=True)
            url = "{url}?{params}".format(url=url, params=parameters)

        status_code, body, response_headers = HTTPClient._get(url, headers, rate_limiter, connection)

        content_type = response_headers.get("Content-Type", "application/octet-stream").upper()

        # Decode to text if a charset is included
        match = re.search("CHARSET=(\S+)", content_type)
        if match:
            encoding = match.group(1)
            body = body.decode(encoding)

            # Load JSON if necessary
            if "APPLICATION/JSON" in content_type:
                body = json.loads(body)

        # Handle errors
        if status_code >= 400:
            if isinstance(body, dict):
                message = body.get("status", {}).get("message", "")
            elif isinstance(body, str):
                message = body
            else:
                message = ""

            raise HTTPError(message, status_code, response_headers)

        return body, response_headers

    @contextmanager
    def new_session(self) -> Curl:
        session = Curl()
        yield session
        session.close()
