from abc import abstractmethod
from typing import MutableMapping, Any, Union, TypeVar, Iterable, Type
try:
    import ujson as json
except ImportError:
    import json

from datapipelines import DataSource, PipelineContext

from ..common import HTTPClient, HTTPError, Curl
from ..riotapi.common import APIForbiddenError, APINotFoundError, APIRequestError, APIError, _ERROR_CODES
from ...dto.staticdata.realm import RealmDto


def _get_latest_version(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    realms = pipeline.get(RealmDto, {"platform": query["platform"]})
    return realms["v"]


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


T = TypeVar("T")


class KernelSource(DataSource):
    def __init__(self, server_url: str, port: int, http_client: HTTPClient = None):
        self._server_url = server_url
        self._port = port
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

    def _get(self, endpoint: str, parameters: MutableMapping[str, Any] = None, connection: Curl = None) -> Union[dict, list, Any]:
        url = f"{self._server_url}:{self._port}/{endpoint}"
        try:
            result, headers = self._client.get(url=url, parameters=parameters, connection=connection)

            # Ensure compatibility with both Curl and Requests based clients
            if isinstance(result, bytes):
                result = json.loads(result.decode())
            elif isinstance(result, str):
                result = json.loads(result)
            
            if not isinstance(result, dict):
                raise ValueError("Unexpected type returned from HTTPClient: {}".format(type(result)))
        except HTTPError as error:
            # The error handlers didn't work, so raise an appropriate error.
            new_error_type = _ERROR_CODES[error.code]
            if new_error_type is RuntimeError:
                new_error = RuntimeError("Encountered an HTTP error code {code} with message \"{message}\" which should have already been handled. Report this to the Cassiopeia team.".format(code=error.code, message=str(error)))
            elif new_error_type is APIError:
                new_error = APIError("Kernel experienced an internal error on the request. You may want to retry the request after a short wait or continue without the result. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APINotFoundError:
                new_error = APINotFoundError("Kernel returned a NOT FOUND error for the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APIRequestError:
                new_error = APIRequestError("Kernel returned an error on the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            elif new_error_type is APIForbiddenError:
                new_error = APIForbiddenError("Kernel returned a FORBIDDEN error for the request. The received error was {code}: \"{message}\"".format(code=error.code, message=str(error)), error.code)
            else:
                new_error = new_error_type(str(error))

            raise new_error from error
        return result

    @abstractmethod
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @abstractmethod
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass
