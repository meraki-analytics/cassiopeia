from abc import abstractmethod
from typing import Mapping, Any, Union, TypeVar, Iterable, Type, Dict

from datapipelines import DataSource, PipelineContext
from merakicommons.ratelimits import RateLimiter, FixedWindowRateLimiter, MultiRateLimiter

from ..common import HTTPClient, HTTPError, Curl
from ...data import Platform


class APIRequestError(HTTPError):
    pass


class APIError(HTTPError):
    pass


class APINotFoundError(HTTPError):
    pass


_ERROR_CODES = {
    400: APIRequestError,
    403: APIRequestError,
    404: APINotFoundError,
    415: RuntimeError,
    429: RuntimeError,
    500: APIError,
    503: APIError
}

T = TypeVar("T")


class RiotAPIService(DataSource):
    def __init__(self, api_key: str, http_client: HTTPClient = None, application_rate_limiters: Dict[Platform, RateLimiter] = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._headers = {
            "X-Riot-Token": api_key
        }

        self._application_rate_limiters = application_rate_limiters
        self._service_rate_limiters = {}

    def _rate_limiter(self, platform: Platform, endpoint: str):
        if self._service_rate_limiters is None:
            return None

        try:
            limiter = self._service_rate_limiters[(platform, endpoint)]
        except KeyError:
            # TODO: Move to settings and don't force dev limits. Also include method rate limiter.
            try:
                limiter = self._application_rate_limiters[platform]
            except KeyError:
                limiter = MultiRateLimiter(FixedWindowRateLimiter(10, 10), FixedWindowRateLimiter(600, 500))
                self._application_rate_limiters[platform] = limiter
            self._service_rate_limiters[(Platform, endpoint)] = limiter
        return limiter

    def _get(self, url: str, parameters: Mapping[str, Any] = None, rate_limiter: RateLimiter = None, connection: Curl = None) -> Union[dict, list, Any]:
        try:
            body, _ = self._client.get(url, parameters, self._headers, rate_limiter, connection)
            return body
        except HTTPError as error:
            try:
                new_error_type = _ERROR_CODES[error.code]
            except KeyError as error2:
                raise RuntimeError("Encountered unexpected HTTP error code {code} with message \"{message}\". Report this to the Cassiopeia team.".format(code=error.code, message=str(error))) from error2

            if new_error_type is RuntimeError:
                new_error = RuntimeError("Encountered an HTTP error code {code} with message \"{message}\" which should have already been handled. Report this to the Cassiopeia team.".format(code=error.code, message=str(error)))
            elif new_error_type is APIError:
                new_error = APIError("The Riot API experienced an internal error on the request. You may want to retry the request after a short wait or continue without the result. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APINotFoundError:
                new_error = APINotFoundError("The Riot API returned a NOT FOUND error for the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APIRequestError:
                new_error = APIRequestError("The Riot API returned an error on the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            else:
                new_error = new_error_type(str(error))

            raise new_error from error

    @abstractmethod
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @abstractmethod
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass
