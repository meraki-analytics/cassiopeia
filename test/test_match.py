import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_matches_return_type():
    matches = cassiopeia.get_matches(SUMMONER_NAME)

    assert isinstance(matches, SearchableList)
    assert all(isinstance(m, cassiopeia.Match) for m in matches)


def test_matches_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        cassiopeia.get_matches(SUMMONER_NAME)


def test_match_correct_return():
    matches = cassiopeia.get_matches(SUMMONER_NAME)
    first_match = matches[0]
    first_match_data = first_match._data[cassiopeia.MatchData]._dto

    match_from_id = cassiopeia.get_match(first_match.id)
    match_from_id_data = match_from_id._data[cassiopeia.MatchData]._dto

    assert isinstance(match_from_id, cassiopeia.Match)
    assert first_match_data == match_from_id_data
