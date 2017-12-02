import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_matches_return_type():
    match_history = cassiopeia.get_match_history(summoner=SUMMONER_NAME, region="NA")

    assert isinstance(match_history, SearchableList)
    assert all(isinstance(m, cassiopeia.Match) for m in match_history)


def test_matches_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        match_history = cassiopeia.get_match_history(summoner=UNKNOWN_SUMMONER_NAME, region="NA")
        match = match_history[0]


def test_match_correct_return():
    match_history = cassiopeia.get_match_history(summoner=SUMMONER_NAME, region="NA")
    first_match = match_history[0]

    match_from_id = cassiopeia.get_match(id=first_match.id, region="NA")

    assert isinstance(match_from_id, cassiopeia.Match)
    assert first_match.id == match_from_id.id
    assert first_match == match_from_id
