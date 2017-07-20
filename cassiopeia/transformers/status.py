from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.status import ShardStatusData

from ..dto.status import ShardStatusDto

T = TypeVar("T")
F = TypeVar("F")


class StatusTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(ShardStatusDto, ShardStatusData)
    def profile_icon_dto_to_data(self, value: ShardStatusDto, context: PipelineContext = None) -> ShardStatusData:
        data = deepcopy(value)
        return ShardStatusData(data)

