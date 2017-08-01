from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.masterypage import MasteryPageData, MasteryPagesData, MasteryPage, MasteryPages
from ..dto.masterypage import MasteryPageDto, MasteryPagesDto

T = TypeVar("T")
F = TypeVar("F")


class MasteriesTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(MasteryPageDto, MasteryPageData)
    def mastery_page_dto_to_data(self, value: MasteryPageDto, context: PipelineContext = None) -> MasteryPageData:
        data = deepcopy(value)
        return MasteryPageData.from_dto(data)

    @transform.register(MasteryPagesDto, MasteryPagesData)
    def mastery_pages_dto_to_data(self, value: MasteryPagesDto, context: PipelineContext = None) -> MasteryPagesData:
        data = deepcopy(value)
        for page in data["pages"]:
            page["region"] = data["region"]
            page["summonerId"] = data["summonerId"]
        data = [self.mastery_page_dto_to_data(page) for page in data["pages"]]
        return MasteryPagesData(data, summoner_id=value["summonerId"])

    # Data to Core

    @transform.register(MasteryPageData, MasteryPage)
    def mastery_page_data_to_core(self, value: MasteryPageData, context: PipelineContext = None) -> MasteryPage:
        data = deepcopy(value)
        return MasteryPage.from_data(data)

    @transform.register(MasteryPagesData, MasteryPages)
    def mastery_pages_data_to_core(self, value: MasteryPagesData, context: PipelineContext = None) -> MasteryPages:
        return MasteryPages([self.mastery_page_data_to_core(page) for page in value], summoner=value.summoner_id)

    # Core to Dto

    @transform.register(MasteryPage, MasteryPageDto)
    def mastery_page_core_to_dto(self, value: MasteryPage, context: PipelineContext = None) -> MasteryPageDto:
        return value._data[MasteryPageData]._dto

    @transform.register(MasteryPages, MasteryPagesDto)
    def mastery_pages_core_to_dto(self, value: MasteryPages, context: PipelineContext = None) -> MasteryPagesDto:
        return MasteryPagesDto({"pages": set([self.mastery_page_core_to_dto(page) for page in value]), "summonerId": value._MasteryPages__summoner.id})
