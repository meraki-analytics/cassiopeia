from typing import Type, TypeVar

from datapipelines import DataTransformer, PipelineContext

from ..core.account import AccountData, Account
from ..dto.account import AccountDto

T = TypeVar("T")
F = TypeVar("F")


class AccountTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(
        self, target_type: Type[T], value: F, context: PipelineContext = None
    ) -> T:
        pass

    # Dto to Data

    @transform.register(AccountDto, AccountData)
    def account_dto_to_data(
        self, value: AccountDto, context: PipelineContext = None
    ) -> AccountData:
        return AccountData(**value)

    # Data to Core

    # @transform.register(AccountData, Account)
    def account_data_to_core(
        self, value: AccountData, context: PipelineContext = None
    ) -> Account:
        return Account.from_data(value)
