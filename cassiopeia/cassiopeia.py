from typing import List, Union
import datetime

from .data import PATCHES, Region, Queue
from .patches import Patch
from .core import Champion, Summoner, Account, ChampionMastery, Rune, Mastery, Item, RunePage, MasteryPage, Match, Map, SummonerSpell, Realms, ProfileIcon, LanguageStrings, CurrentMatch, ShardStatus, Versions, MatchHistory, Champions, ChampionMasteries, Masteries, Runes, Items, SummonerSpells, Maps, FeaturedMatches, Locales, ProfileIcons, MasteryPages, RunePages, ChallengerLeague, MasterLeague, Leagues


def get_leagues(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) -> Leagues:
    return Leagues(summoner=summoner, region=region)


def get_master_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> MasterLeague:
    return MasterLeague(queue=queue, region=region)


def get_challenger_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> ChallengerLeague:
    return ChallengerLeague(queue=queue, region=region)


def get_match_history(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) -> MatchHistory:
    return MatchHistory(summoner=summoner, region=region)


def get_match(id, region: Union[Region, str] = None) -> Match:
    return Match(id=id, region=region)


def get_featured_matches(region: Union[Region, str] = None) -> FeaturedMatches:
    return FeaturedMatches(region=region)


def get_current_match(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) ->  CurrentMatch:
    return CurrentMatch(summoner=summoner, region=region)


def get_champion_masteries(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) -> ChampionMasteries:
    return ChampionMasteries(summoner=summoner, region=region)


def get_champion_mastery(summoner: Union[Summoner, int, str], champion: Union[Champion, int, str], region: Union[Region, str] = None) -> ChampionMastery:
    return ChampionMastery(champion=champion, summoner=summoner, region=region)


def get_summoner(*, id: int = None, account: Union[Account, int] = None, name: str = None, region: Union[Region, str] = None) -> Summoner:
    return Summoner(id=id, account=account, name=name, region=region)


def get_champion(key: Union[str, int], region: Union[Region, str] = None) -> Champion:
    return get_champions(region=region)[key]


def get_champions(region: Union[Region, str] = None) -> List[Champion]:
    return Champions(region=region)


def get_masteries(region: Union[Region, str] = None) -> List[Mastery]:
    return Masteries(region=region)


def get_runes(region: Union[Region, str] = None) -> List[Rune]:
    return Runes(region=region)


def get_summoner_spells(region: Union[Region, str] = None) -> List[SummonerSpell]:
    return SummonerSpells(region=region)


def get_items(region: Union[Region, str] = None) -> List[Item]:
    return Items(region=region)


def get_mastery_pages(summoner: Summoner, region: Union[Region, str] = None) -> List[MasteryPage]:
    return MasteryPages(summoner=summoner, region=region)


def get_rune_pages(summoner: Summoner, region: Union[Region, str] = None) -> List[RunePage]:
    return RunePages(summoner=summoner, region=region)


def get_maps(region: Union[Region, str] = None) -> List[Map]:
    return Maps(region=region)


def get_profile_icons(region: Union[Region, str] = None) -> List[ProfileIcon]:
    return ProfileIcons(region=region)


def get_realms(region: Union[Region, str] = None) -> Realms:
    return Realms(region=region)


def get_status(region: Union[Region, str] = None) -> ShardStatus:
    return ShardStatus(region=region)


def get_language_strings(region: Union[Region, str] = None) -> LanguageStrings:
    return LanguageStrings(region=region)


def get_locales(region: Union[Region, str] = None) -> List[str]:
    return Locales(region=region)


def get_versions(region: Union[Region, str] = None) -> List[str]:
    return Versions(region=region)


def get_version(date: datetime.date = None, region: Union[Region, str] = None) -> Union[None, str]:
    versions = get_versions(region)
    if date is None:
        return versions[0]
    else:
        patch = get_patch(date)
        for version in versions:
            if patch.majorminor in version:
                return version
    return None


def get_patch(date: datetime.date) -> Patch:
    for _date in PATCHES:
        if _date >= date:
            return PATCHES[_date]
    return PATCHES[next(reversed(PATCHES))]
