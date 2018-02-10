from typing import List, Set, Dict, Union, TextIO
import arrow
import datetime

from .data import Region, Queue, Season
from .core import Champion, Summoner, Account, ChampionMastery, Rune, Item, Match, Map, SummonerSpell, Realms, ProfileIcon, LanguageStrings, CurrentMatch, ShardStatus, Versions, MatchHistory, Champions, ChampionMasteries, Runes, Items, SummonerSpells, Maps, FeaturedMatches, Locales, ProfileIcons, ChallengerLeague, MasterLeague, SummonerLeagues, LeagueEntries, Patch, VerificationString
from .datastores import common as _common_datastore
from ._configuration import Settings, load_config, get_default_config
from . import configuration


# Settings endpoints

def apply_settings(config: Union[str, TextIO, Dict, Settings]):
    if not isinstance(config, (Dict, Settings)):
        config = load_config(config)
    if not isinstance(config, Settings):
        settings = Settings(config)
    else:
        settings = config

    # Load any plugins after everything else has finished importing
    import importlib
    for plugin in settings.plugins:
        imported_plugin = importlib.import_module("cassiopeia.plugins.{plugin}.monkeypatch".format(plugin=plugin))

    print_calls(settings._Settings__default_print_calls, settings._Settings__default_print_riot_api_key)

    # Overwrite the old settings
    configuration._settings = settings


def set_riot_api_key(key: str):
    configuration.settings.set_riot_api_key(key)


def set_default_region(region: Union[Region, str]):
    configuration.settings.set_region(region)


def print_calls(calls: bool, api_key: bool = False):
    _common_datastore._print_calls = calls
    _common_datastore._print_api_key = api_key


# Data endpoints

def get_league_positions(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) -> LeagueEntries:
    if not isinstance(summoner, Summoner):
        if isinstance(summoner, int):
            summoner = Summoner(id=summoner, region=region)
        else:
            summoner = Summoner(name=summoner, region=region)
    return summoner.league_positions


def get_leagues(summoner: Union[Summoner, int, str], region: Union[Region, str] = None) -> SummonerLeagues:
    if not isinstance(summoner, Summoner):
        if isinstance(summoner, int):
            summoner = Summoner(id=summoner, region=region)
        else:
            summoner = Summoner(name=summoner, region=region)
    return summoner.leagues


def get_master_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> MasterLeague:
    return MasterLeague(queue=queue, region=region)


def get_challenger_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> ChallengerLeague:
    return ChallengerLeague(queue=queue, region=region)


def get_match_history(summoner: Union[Summoner, str, int] = None, region: Union[Region, str] = None, begin_index: int = None, end_index: int = None, begin_time: arrow.Arrow = None, end_time: arrow.Arrow = None, queues: Set[Queue] = None, seasons: Set[Season] = None, champions: Set[Champion] = None):
    return MatchHistory(summoner=summoner, begin_index=begin_index, end_index=end_index, begin_time=begin_time, end_time=end_time, queues=queues, seasons=seasons, champions=champions)

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


def get_champions(region: Union[Region, str] = None) -> Champions:
    return Champions(region=region)


def get_runes(region: Union[Region, str] = None) -> Runes:
    return Runes(region=region)


def get_summoner_spells(region: Union[Region, str] = None) -> SummonerSpells:
    return SummonerSpells(region=region)


def get_items(region: Union[Region, str] = None) -> Items:
    return Items(region=region)


def get_maps(region: Union[Region, str] = None) -> Maps:
    return Maps(region=region)


def get_profile_icons(region: Union[Region, str] = None) -> ProfileIcons:
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
        patch = Patch.from_date(date, region=region)
        for version in versions:
            if patch.majorminor in version:
                return version
    return None


def get_verification_string(summoner: Summoner) -> VerificationString:
    return VerificationString(summoner=summoner)
