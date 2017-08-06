from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.status import ShardStatusData, ShardStatus
from ..dto.status import ShardStatusDto

T = TypeVar("T")
F = TypeVar("F")


class StatusTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(ShardStatusDto, ShardStatusData)
    def shard_status_dto_to_data(self, value: ShardStatusDto, context: PipelineContext = None) -> ShardStatusData:
        data = deepcopy(value)
        return ShardStatusData.from_dto(data)

    # Data to Core

    @transform.register(ShardStatusData, ShardStatus)
    def shard_status_data_to_core(self, value: ShardStatusData, context: PipelineContext = None) -> ShardStatus:
        return ShardStatus.from_data(value)

    # Core to Dto

    @transform.register(ShardStatus, ShardStatusDto)
    def shard_status_core_to_dto(self, value: ShardStatus, context: PipelineContext = None) -> ShardStatusDto:
        return value[ShardStatusData]._dto
