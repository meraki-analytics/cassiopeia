import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import CHAMP_NAME, SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_masteries_correct_type():
    champ_masteries = cassiopeia.get_champion_masteries(SUMMONER_NAME)

    assert isinstance(champ_masteries, SearchableList)
    assert all(isinstance(cm, cassiopeia.ChampionMastery) for cm in champ_masteries)


def test_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        cassiopeia.get_champion_masteries(UNKNOWN_SUMMONER_NAME)


def test_masteries_with_id_or_summoner():
    summ = cassiopeia.get_summoner(name=SUMMONER_NAME)

    from_summoner = set(cassiopeia.get_champion_masteries(summ))
    from_id = set(cassiopeia.get_champion_masteries(summ.id))
    from_name = set(cassiopeia.get_champion_masteries(summ.name))

    assert from_summoner == from_id
    assert from_id == from_name


def test_mastery_return():
    champ_mastery = cassiopeia.get_champion_mastery(summoner=SUMMONER_NAME, champion=CHAMP_NAME)

    assert isinstance(champ_mastery, cassiopeia.ChampionMastery)
    assert isinstance(champ_mastery.summoner, cassiopeia.Summoner)
    assert isinstance(champ_mastery.champion, cassiopeia.Champion)

    assert champ_mastery.summoner.name == SUMMONER_NAME
    assert champ_mastery.champion.name == CHAMP_NAME


def test_mastery_returns_correct_data():
    masteries = cassiopeia.get_champion_masteries(SUMMONER_NAME)
    on_champ = masteries[0]

    from_single_call = cassiopeia.get_champion_mastery(SUMMONER_NAME, on_champ.champion)

    assert on_champ == from_single_call
