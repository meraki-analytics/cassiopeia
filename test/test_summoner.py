import cassiopeia
import pytest

from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        cassiopeia.get_summoner(UNKNOWN_SUMMONER_NAME)


def test_raises_with_id_as_name():
    with pytest.raises(NameError):
        cassiopeia.get_summoner(1337)


def test_return_type():
    summ = cassiopeia.get_summoner(SUMMONER_NAME)

    assert isinstance(summ, cassiopeia.Summoner)


def test_equal_result_with_summoner_id():
    from_name = cassiopeia.get_summoner(SUMMONER_NAME)
    from_name_data = from_name._data[cassiopeia.Summoner]._dto
    from_id = cassiopeia.get_summoner(id=from_name.id)
    from_id_data = from_id._data[cassiopeia.Summoner]._dto

    assert from_name_data == from_id_data
