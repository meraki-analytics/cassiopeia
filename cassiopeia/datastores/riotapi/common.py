import time
from abc import abstractmethod
from typing import MutableMapping, Any, Union, TypeVar, Iterable, Type, Dict
from collections import defaultdict

from datapipelines import DataSource, PipelineContext, NotFoundError
from merakicommons.ratelimits import RateLimiter, FixedWindowRateLimiter, MultiRateLimiter

from ..common import HTTPClient, HTTPError, Curl
from ...data import Platform


class APIRequestError(HTTPError):
    pass


class APIError(HTTPError):
    pass


class APINotFoundError(HTTPError):
    pass


class APIForbiddenError(APINotFoundError):
    pass


_ERROR_CODES = {
    400: APIRequestError,
    401: APIForbiddenError,
    403: APIRequestError,
    404: APINotFoundError,
    415: RuntimeError,
    429: RuntimeError,
    500: APIError,
    503: APIError
}

T = TypeVar("T")


_METHOD_RATE_LIMITS = defaultdict(lambda: (20000, 10))
_METHOD_RATE_LIMITS.update({
    "matches/id": (500, 10),
    "timelines/by-match/id": (500, 10),
    "matchlists/by-account/accountId": (1000, 10),
    "matchlists/by-account/accountId/recent": (1000, 10),
    "staticdata/champion": (10, 3600),
    "staticdata/champions": (10, 3600),
    "staticdata/versions": (10, 3600),
    "staticdata/mastery": (10, 3600),
    "staticdata/masteries": (10, 3600),
    "staticdata/rune": (10, 3600),
    "staticdata/runes": (10, 3600),
    "staticdata/item": (10, 3600),
    "staticdata/items": (10, 3600),
    "staticdata/maps": (10, 3600),
    "staticdata/summoner-spell": (10, 3600),
    "staticdata/summoner-spells": (10, 3600),
    "staticdata/realms": (10, 3600),
    "staticdata/language": (10, 3600),
    "staticdata/language-strings": (10, 3600),
    "staticdata/profile-icons": (10, 3600),
    "masteries/by-summoner/summonerId": (400, 60),
    "runes/by-summoner/summonerId": (400, 60),
    "champions": (400, 60)
})


def _split_rate_limit_header(header):
    rates = []
    for pw in header.split(","):
        pw = pw.split(":")
        p, w = pw
        p, w = int(p), int(w)
        rates.append((p,w))
    return rates


class RiotAPIService(DataSource):
    def __init__(self, api_key: str, http_client: HTTPClient = None, application_rate_limiters: Dict[Platform, RateLimiter] = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._headers = {
            "X-Riot-Token": api_key
        }

        # Both the application and method rate limiters will be in the same rate limiter
        self._rate_limiters = application_rate_limiters or {}

    def _get_rate_limiter(self, platform: Platform, endpoint: str):
        try:
            limiter = self._rate_limiters[(platform, endpoint)]
        except KeyError:
            # TODO: Move to settings and don't force dev limits.
            # TODO This is a circular import and instead this functionality should somehow be moved into settings.
            from cassiopeia.configuration import settings
            limits = settings.rate_limits
            limiter = MultiRateLimiter(*(
                [FixedWindowRateLimiter(window, permits) for permits, window in limits] +
                [FixedWindowRateLimiter(*reversed(_METHOD_RATE_LIMITS[endpoint]))]
            ))
            self._rate_limiters[(platform, endpoint)] = limiter
        return limiter

    def _get(self, url: str, parameters: MutableMapping[str, Any] = None, rate_limiter: MultiRateLimiter = None, connection: Curl = None, backoff: float = 1.) -> Union[dict, list, Any]:
        try:
            body, response_headers = self._client.get(url, parameters, self._headers, rate_limiter, connection)

            # If Riot changes the # of permits allowed in their response headers, change our rate limiters.
            # If any windows aren't of the correct length, they won't be updated / changed, so we throw an error if we
            #   receive a window for which the user (or the method rate limiter) doesn't have a set number of permits.
            # TODO This will override any user settings for this specific window.
            # We are currently ignoring the X-*-Rate-Limit-Count headers and assuming our rate limiter logic agrees.
            found = False
            if "X-App-Rate-Limit" in response_headers:
                for permits, window in _split_rate_limit_header(response_headers["X-App-Rate-Limit"]):
                    for _rate_limiter in rate_limiter:
                        if window == _rate_limiter._window_seconds:
                            if permits != _rate_limiter._window_permits:
                                _rate_limiter.set_permits(permits)
                            found = True
                            break
                    if found:
                        break
                else:
                    raise RuntimeError("Users must provide a rate limit for each window that Riot provides a rate limit for. The rate limits we received were: {}".format(
                        _split_rate_limit_header(response_headers["X-App-Rate-Limit"])
                    ))
            found = False
            if "X-Method-Rate-Limit" in response_headers:
                for permits, window in _split_rate_limit_header(response_headers["X-Method-Rate-Limit"]):
                    for _rate_limiter in rate_limiter:
                        if window == _rate_limiter._window_seconds:
                            if permits != _rate_limiter._window_permits:
                                _rate_limiter.set_permits(permits)
                            found = True
                            break
                    if found:
                        break
                else:
                    raise RuntimeError("Users must provide a rate limit for each window that Riot provides a rate limit for. The rate limits we received were: {}".format(
                        _split_rate_limit_header(response_headers["X-Method-Rate-Limit"])
                    ))

            return body
        except HTTPError as error:
            try:
                new_error_type = _ERROR_CODES[error.code]
            except KeyError as error2:
                raise RuntimeError("Encountered unexpected HTTP error code {code} with message \"{message}\". Report this to the Cassiopeia team.".format(code=error.code, message=str(error))) from error2

            # Try to properly handling the 429 and retry the call after the appropriate time limit.
            if error.code == 429:
                if "X-Rate-Limit-Type" not in error.response_headers or error.response_headers["X-Rate-Limit-Type"] == "service":
                    # Back off for one or more seconds
                    time.sleep(backoff)
                    if backoff < 3:  # Backoff at most 3 times, then quit
                        print("INFO: Unexpected service rate limit, backing off for {} seconds.".format(backoff))
                        return self._get(url, parameters, rate_limiter, connection, backoff + 1)  # Backoff for 1 more second each time. This isn't exponential backoff but it's probably fine.
                else:
                    if error.response_headers["X-Rate-Limit-Type"] == "application":
                        print("WARNING: Unexpected 429 due to application rate limit.")
                        if backoff < 3:  # Backoff isn't directly, here we're using it simply to prevent blacklisting if something in our code is wrong
                            rate_limiter.restrict_for(error.response_headers["Retry-After"])
                            return self._get(url, parameters, rate_limiter, connection, backoff + 1)  # Backoff for 1 more second each time. This isn't exponential backoff but it's probably fine.
                    elif error.response_headers["X-Rate-Limit-Type"] == "method":
                        print("WARNING: Unexpected 429 due to method rate limit.")
                        if backoff < 3:  # Backoff isn't directly, here we're using it simply to prevent blacklisting if something in our code is wrong
                            rate_limiter.restrict_for(error.response_headers["Retry-After"])
                            return self._get(url, parameters, rate_limiter, connection, backoff + 1)  # Backoff for 1 more second each time. This isn't exponential backoff but it's probably fine.
                    else:
                        raise RuntimeError("Unknown response header value for `X-Rate-Limit-Type`: {}".format(error.response_headers["X-Rate-Limit-Type"]))

            # The above error handling didn't work, so raise an appropriate error.
            if new_error_type is RuntimeError:
                new_error = RuntimeError("Encountered an HTTP error code {code} with message \"{message}\" which should have already been handled. Report this to the Cassiopeia team.".format(code=error.code, message=str(error)))
            elif new_error_type is APIError:
                new_error = APIError("The Riot API experienced an internal error on the request. You may want to retry the request after a short wait or continue without the result. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APINotFoundError:
                new_error = APINotFoundError("The Riot API returned a NOT FOUND error for the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APIRequestError:
                new_error = APIRequestError("The Riot API returned an error on the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APIForbiddenError:
                new_error = APIForbiddenError("The Riot API returned a FORBIDDEN error for the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            else:
                new_error = new_error_type(str(error))

            raise new_error from error

    @abstractmethod
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @abstractmethod
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass
