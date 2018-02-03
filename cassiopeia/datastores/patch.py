from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, NotFoundError

from ..dto.patch import PatchListDto
from .common import HTTPClient, HTTPError

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class PatchSource(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    ##############
    # Patch List #
    ##############

    @get.register(PatchListDto)
    def get_patch_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> PatchListDto:
        # See: https://rawgit.com/
        url = "https://cdn.rawgit.com/meraki-analytics/cassiopeia/662a3edf/cassiopeia/patches.json"
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        return PatchListDto(**body)
