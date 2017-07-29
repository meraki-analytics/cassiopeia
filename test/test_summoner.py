import cassiopeia
import pytest

from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_unknown_summoner():
    assert not cassiopeia.get_summoner(name=UNKNOWN_SUMMONER_NAME).exists
    assert not cassiopeia.get_summoner(id=9999999999999).exists


def test_equal_result_with_summoner_id():
    from_name = cassiopeia.get_summoner(name=SUMMONER_NAME)
    from_id = cassiopeia.get_summoner(id=from_name.id)

    assert from_name.id == from_id.id
