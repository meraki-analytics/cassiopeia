from typing import Type, TypeVar, Mapping, Any, Iterable, Union
import requests

from datapipelines import DataSource, PipelineContext, Query

from .common import HTTPClient, HTTPError, Curl
from ..core.datadragon import DataDragonImage

T = TypeVar("T")

class DataDragonService(DataSource):
    def __init__(self, http_client: HTTPClient = None):
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

    def _get(self, url: str, parameters: Mapping[str, Any] = None, connection: Curl = None) -> Union[dict, list, Any]:
        body, _ = self._client.get(url, parameters or {}, connection)
        return body

    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_image = Query. \
        has("url").as_(str)

    @get.register(DataDragonImage)
    def get_image(self, query: Mapping[str, Any], context: PipelineContext = None) -> DataDragonImage:
        DataDragonService._validate_get_image(query, context)
        raw = requests.get(query["url"], stream=True).raw
        raw.decode_content = True
        return raw
