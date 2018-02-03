import arrow

import cassiopeia
from cassiopeia import Region, Platform
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError

from .constants import CHAMP_NAME, SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


def test_masteries_correct_type():
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
    champ_masteries = cassiopeia.get_champion_masteries(summoner=summoner.id, region="NA")

    assert isinstance(champ_masteries, SearchableList)
    assert all(isinstance(cm, cassiopeia.ChampionMastery) for cm in champ_masteries)


def test_masteries_contains_all_champions():
    champions = cassiopeia.get_champions(region="NA")
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
    champ_masteries = cassiopeia.get_champion_masteries(summoner=summoner.id, region="NA")
    for cm in champ_masteries:
        assert cm.champion in champions
    for champion in champions:
        assert champion in champ_masteries


def test_mastery_return():
    summoner = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
    champion = cassiopeia.get_champion(CHAMP_NAME, region="NA")
    champion_mastery = cassiopeia.get_champion_mastery(summoner=summoner.id, champion=champion, region="NA")

    assert isinstance(champion_mastery, cassiopeia.ChampionMastery)
    assert isinstance(champion_mastery.summoner, cassiopeia.Summoner)
    assert isinstance(champion_mastery.champion, cassiopeia.Champion)

    assert champion_mastery.summoner == summoner
    assert champion_mastery.champion == champion

    assert isinstance(champion_mastery.platform, Platform)
    assert isinstance(champion_mastery.region, Region)
    assert isinstance(champion_mastery.chest_granted, bool)
    assert isinstance(champion_mastery.last_played, arrow.Arrow)
    assert isinstance(champion_mastery.level, int) and champion_mastery.level <= 7
    assert isinstance(champion_mastery.points, int)
    assert isinstance(champion_mastery.points_since_last_level, int)
    assert isinstance(champion_mastery.points_until_next_level, int)
