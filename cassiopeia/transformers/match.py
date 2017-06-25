from typing import Type, TypeVar, MutableMapping, Any
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.match import MatchData, MatchListData, MatchReferenceData
from ..dto.match import MatchDto, MatchListDto, MatchReferenceDto

T = TypeVar("T")
F = TypeVar("F")


class MatchTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(MatchReferenceDto, MatchReferenceData)
    def match_reference_dto_to_core(self, value: MatchReferenceDto, context: PipelineContext = None) -> MatchReferenceData:
        data = deepcopy(value)
        return MatchReferenceData(data)

    @transform.register(MatchDto, MatchData)
    def match_dto_to_core(self, value: MatchDto, context: PipelineContext = None) -> MatchData:
        data = deepcopy(value)
        return MatchData(data)

    @transform.register(MatchListDto, MatchListData)
    def matchlist_dto_to_core(self, value: MatchListDto, context: PipelineContext = None) -> MatchListData:
        data = deepcopy(value)
        data = data["matches"]
        return MatchListData([self.match_reference_dto_to_core(match) for match in data])
