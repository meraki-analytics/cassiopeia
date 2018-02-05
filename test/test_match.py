import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_matches_return_type():
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
    match_history = cassiopeia.get_match_history(summoner=summoner)

    assert isinstance(match_history, SearchableList)
    assert all(isinstance(m, cassiopeia.Match) for m in match_history)


def test_matches_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        summoner = cassiopeia.get_summoner(name=UNKNOWN_SUMMONER_NAME, region="NA")
        match_history = cassiopeia.get_match_history(summoner=summoner)
        match = match_history[0]


def test_match_correct_return():
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
    match_history = cassiopeia.get_match_history(summoner=summoner)
    first_match = match_history[0]

    match_from_id = cassiopeia.get_match(id=first_match.id, region="NA")

    assert isinstance(match_from_id, cassiopeia.Match)
    assert first_match.id == match_from_id.id
    assert first_match == match_from_id


def test_match_participant_search():
    summoner = cassiopeia.Summoner(name='Kejorn', region='NA')
    match = summoner.match_history[0]
    p = match.participants[summoner]
