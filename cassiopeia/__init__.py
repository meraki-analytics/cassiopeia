# Initialize the settings singleton
from ._configuration import get_default_config, Settings, CassiopeiaConfiguration as _CassiopeiaConfiguration
configuration = _CassiopeiaConfiguration()

from .cassiopeia import get_realms, get_challenger_league, get_champion_masteries, get_champion, get_champion_mastery, get_champions, get_current_match, get_featured_matches, get_items, get_language_strings, get_locales, get_league_positions, get_leagues, get_maps, get_master_league, get_match, get_match_history, get_profile_icons, get_runes, get_status, get_summoner, get_summoner_spells, get_version, get_versions
from .cassiopeia import apply_settings, set_riot_api_key, set_default_region, print_calls
from .core import Champion, Champions, Rune, Runes, Item, Items, SummonerSpell, SummonerSpells, ProfileIcon, ProfileIcons, Versions, Maps, Summoner, Account, ChampionMastery, ChampionMasteries, Match, FeaturedMatches, ShardStatus, ChallengerLeague, MasterLeague, Map, Realms, LanguageStrings, Locales, LeagueEntries, League, Patch, VerificationString
from .data import Queue, Region, Platform, Resource, Side, GameMode, MasteryTree, RunePath, Tier, Division, Season, GameType, Lane, Role

apply_settings(configuration.settings)
