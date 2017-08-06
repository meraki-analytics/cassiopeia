from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator
from io import BytesIO

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from PIL import Image as ImageLoader
from PIL.Image import Image

from .common import HTTPClient

T = TypeVar("T")


class ImageDataSource(DataSource):
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

    _validate_get_image = Query. \
        has("url").as_(str)

    @get.register(Image)
    def get_image(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Image:
        ImageDataSource._validate_get_image(query, context)
        try:
            data, _ = self._client.get(query["url"])
            return ImageLoader.open(BytesIO(data))
        except Exception as e:
            raise NotFoundError(str(e)) from e

    _validate_get_many_image = Query. \
        has("urls").as_(Iterable)

    @get_many.register(Image)
    def get_many_image(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[Image, None, None]:
        ImageDataSource._validate_get_many_image(query, context)

        def generator():
            for url in query["urls"]:
                if not isinstance(url, str):
                    raise NotFoundError("urls must be strings!")

                try:
                    data, _ = self._client.get(url)
                    yield ImageLoader.open(BytesIO(data))
                except Exception as e:
                    raise NotFoundError(str(e)) from e

        return generator()
