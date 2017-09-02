import os
import pickle
from abc import abstractmethod
from typing import Mapping, Any, TypeVar, Iterable, Type
from simplekv.fs import FilesystemStore

from datapipelines import DataSource, DataSink, PipelineContext, NotFoundError

from ...dto.common import DtoObject

T = TypeVar("T")


class SimpleKVDiskService(DataSource, DataSink):
    def __init__(self):
        this_direc, _ = os.path.split(os.path.abspath(__file__))
        kvstore_fn = os.path.join(this_direc, "..", "..", "..", "simplekv_store")  # path/to/top/level/cassiopeia/simplekv_store
        if not os.path.exists(kvstore_fn):
            os.mkdir(kvstore_fn)
        self._store = FilesystemStore(kvstore_fn)
        self.encoding = "utf-8"

    @abstractmethod
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @abstractmethod
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @abstractmethod
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @abstractmethod
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    def _get(self, key: str):
        try:
            data = pickle.loads(self._store.get(key))
        except KeyError:
            raise NotFoundError
        return data

    def _put(self, key: str, item: DtoObject):
        if key not in self._store:
            pickle_item = pickle.dumps(item)
            pickle_item = pickle_item
            self._store.put(key, pickle_item)
