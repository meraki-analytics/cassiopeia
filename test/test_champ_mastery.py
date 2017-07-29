import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import CHAMP_NAME, SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_masteries_correct_type():
    # TODO: Once get_champion_masteries works with passing a name,
    #       replace this with get_champion_masteries(SUMMONER_NAME)
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME)
    champ_masteries = cassiopeia.get_champion_masteries(summoner.id)

    assert isinstance(champ_masteries, SearchableList)
    assert all(isinstance(cm, cassiopeia.ChampionMastery) for cm in champ_masteries)


def test_returns_empty_list_with_unknown_summoner():
    # TODO: Also do this with name, once it's implemented (see above)
    cm = cassiopeia.get_champion_masteries(123901923180391)
    assert cm == []


# def test_masteries_with_id_or_summoner():
    # TODO
    # Comment out these tests once get_champion_masteries supports
    # retrieving mastery through name or summoner again
    # (currently only supports it through ID)

    # summ = cassiopeia.get_summoner(name=SUMMONER_NAME)

    # from_summoner = set(cassiopeia.get_champion_masteries(summ))
    # from_id = set(cassiopeia.get_champion_masteries(summ.id))
    # from_name = set(cassiopeia.get_champion_masteries(summ.name))

    # assert from_summoner == from_id
    # assert from_id == from_name


def test_mastery_return():
    summ = cassiopeia.get_summoner(name=SUMMONER_NAME)
    champ = cassiopeia.get_champion(CHAMP_NAME)
    champ_mastery = cassiopeia.get_champion_mastery(summ.id, champion=champ)

    assert isinstance(champ_mastery, cassiopeia.ChampionMastery)
    assert isinstance(champ_mastery.summoner, cassiopeia.Summoner)
    assert isinstance(champ_mastery.champion, cassiopeia.Champion)

    assert champ_mastery.summoner.name == SUMMONER_NAME
    assert champ_mastery.champion.name == CHAMP_NAME


def test_mastery_returns_correct_data():
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME)
    masteries = cassiopeia.get_champion_masteries(summoner.id)
    on_champ = masteries[0]

    from_single_call = cassiopeia.get_champion_mastery(SUMMONER_NAME, on_champ.champion)

    #assert on_champ._data[cassiopeia.core.championmastery.ChampionMasteryData]._dto == from_single_call._data[cassiopeia.core.championmastery.ChampionMasteryData]._dto
    assert on_champ.points == from_single_call.points

