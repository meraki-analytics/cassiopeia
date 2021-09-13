# Initialize the settings singleton
from ._configuration import get_default_config, Settings, CassiopeiaConfiguration as _CassiopeiaConfiguration
configuration = _CassiopeiaConfiguration()

from .cassiopeia import get_realms, get_challenger_league, get_champion_masteries, get_champion, get_champion_mastery, get_champions, get_current_match, get_featured_matches, get_items, get_language_strings, get_locales, get_league_entries, get_maps, get_master_league, get_grandmaster_league, get_match, get_match_history, get_profile_icons, get_runes, get_status, get_summoner, get_summoner_spells, get_version, get_versions, get_champion_rotations, get_paginated_league_entries, get_verification_string
from .cassiopeia import apply_settings, set_riot_api_key, print_calls, _get_pipeline
from .core import Champion, Champions, Rune, Runes, Item, Items, SummonerSpell, SummonerSpells, ProfileIcon, ProfileIcons, Versions, Maps, Summoner, ChampionMastery, ChampionMasteries, Match, FeaturedMatches, ShardStatus, ChallengerLeague, GrandmasterLeague, MasterLeague, Map, Realms, LanguageStrings, Locales, LeagueEntries, League, Patch, VerificationString, MatchHistory, ChampionRotation, LeagueSummonerEntries, CurrentMatch
from .data import Queue, Region, Platform, Resource, Side, GameMode, MasteryTree, Tier, Division, Season, GameType, Lane, Role, Rank, Key, SummonersRiftArea, Tower, Position

apply_settings(configuration.settings)
