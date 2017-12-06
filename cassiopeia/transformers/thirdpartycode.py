from typing import Type, TypeVar

from datapipelines import DataTransformer, PipelineContext

from ..core.thirdpartycode import VerificationString, VerificationStringData
from ..dto.thirdpartycode import VerificationStringDto

T = TypeVar("T")
F = TypeVar("F")


class ThirdPartyCodeTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(VerificationStringDto, VerificationStringData)
    def verification_string_dto_to_data(self, value: VerificationStringDto, context: PipelineContext = None) -> VerificationStringData:
        return VerificationStringData(**value)

    # Data to Core

    #@transform.register(VerificationStringData, VerificationString)
    def verification_string_data_to_core(self, value: VerificationStringData, context: PipelineContext = None) -> VerificationString:
        return VerificationString.from_data(value)
