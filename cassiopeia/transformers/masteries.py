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
        return MasteryPagesData(data)

    # Data to Core

    @transform.register(MasteryPageData, MasteryPage)
    def mastery_page_data_to_core(self, value: MasteryPageData, context: PipelineContext = None) -> MasteryPage:
        return MasteryPage.from_data(value)

    @transform.register(MasteryPagesData, MasteryPages)
    def mastery_pages_data_to_core(self, value: MasteryPagesData, context: PipelineContext = None) -> MasteryPages:
        return MasteryPages([self.mastery_page_data_to_core(page) for page in value])

    # Core to Dto TODO
