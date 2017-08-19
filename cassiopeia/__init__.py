from .cassiopeia import get_realms, get_challenger_league, get_champion_masteries, get_champion, get_champion_mastery, get_champions, get_current_match, get_featured_matches, get_items, get_language_strings, get_locales, get_league_positions, get_leagues, get_maps, get_master_league, get_masteries, get_mastery_pages, get_match, get_match_history, get_patch, get_profile_icons, get_rune_pages, get_runes, get_status, get_summoner, get_summoner_spells, get_version, get_versions
from .core import Champion, Champions, Rune, Runes, Mastery, Masteries, Item, Items, SummonerSpell, SummonerSpells, ProfileIcon, ProfileIcons, Versions, Maps, Summoner, Account, ChampionMastery, ChampionMasteries, Match, FeaturedMatches, ShardStatus, ChallengerLeague, MasterLeague, Map, Realms, LanguageStrings, Locales, LeagueEntries, Leagues


# Load any plugins after everything else has finished importing

import importlib
from .configuration import settings as _settings


for plugin in _settings.plugins:
    imported_plugin = importlib.import_module("cassiopeia.plugins.{plugin}.monkeypatch".format(plugin=plugin))
