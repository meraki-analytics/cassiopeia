import cassiopeia
import pytest

from datapipelines.common import NotFoundError


def test_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        cassiopeia.get_summoner('abcaklsjdlaksdjlaksjdla')


def test_raises_with_id_as_name():
    with pytest.raises(NameError):
        cassiopeia.get_summoner(1337)


def test_return_type():
    summ = cassiopeia.get_summoner('Kalturi')

    assert isinstance(summ, cassiopeia.Summoner)


def test_equal_result_with_summoner_id():
    from_name = cassiopeia.get_summoner('Kalturi')
    from_name_data = from_name._data[cassiopeia.Summoner]._dto
    from_id = cassiopeia.get_summoner(id=from_name.id)
    from_id_data = from_id._data[cassiopeia.Summoner]._dto

    assert from_name_data == from_id_data