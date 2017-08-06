import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_matches_return_type():
    match_history = cassiopeia.get_match_history(SUMMONER_NAME)

    assert isinstance(match_history, SearchableList)
    assert all(isinstance(m, cassiopeia.Match) for m in match_history)


def test_matches_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        match_history = cassiopeia.get_match_history(UNKNOWN_SUMMONER_NAME)
        match_history[0]


def test_match_correct_return():
    match_history = cassiopeia.get_match_history(SUMMONER_NAME)
    first_match = match_history[0]
    first_match_data = first_match._data[cassiopeia.core.match.MatchData]._dto

    match_from_id = cassiopeia.get_match(first_match.id)
    match_from_id_data = match_from_id._data[cassiopeia.core.match.MatchData]._dto

    assert isinstance(match_from_id, cassiopeia.Match)
    #assert first_match_data == match_from_id_data
    assert first_match.id == match_from_id.id
