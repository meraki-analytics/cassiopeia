from typing import Tuple, Set, Union

from ..dto.champion import ChampionListDto as ChampionStatusListDto, ChampionDto as ChampionStatusDto
from ..dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto, ChampionMasteryScoreDto
from ..dto.league import LeagueListDto, LeaguePositionsDto
from ..dto.staticdata import ChampionDto, ChampionListDto, ItemDto, ItemListDto, LanguageStringsDto, LanguagesDto, MasteryDto, MasteryListDto, ProfileIconDataDto, ProfileIconDetailsDto, RealmDto, RuneDto, RuneListDto, SummonerSpellDto, SummonerSpellListDto, MapDto, MapListDto, VersionListDto
from ..dto.status import ShardStatusDto
from ..dto.masterypage import MasteryPagesDto, MasteryPageDto
from ..dto.match import MatchDto, MatchReferenceDto, MatchTimelineDto
from ..dto.runepage import RunePagesDto, RunePageDto
from ..dto.spectator import CurrentGameInfoDto, FeaturedGamesDto
from ..dto.summoner import SummonerDto

from ..core.championmastery import ChampionMastery
from ..core.league import LeagueSummoner
from ..core.staticdata import Champion, Mastery, Rune, Item, SummonerSpell, Map
from ..core.masterypage import MasteryPage
from ..core.match import Match
from ..core.runepage import RunePage
from ..core.summoner import Summoner

#############
# Utilities #
#############


def _hash_included_data(included_data: Set[str]) -> int:
    return hash(tuple(included_data))


#######
# DTO #
#######


################
# Champion API #
################


def for_champion_status_dto(champion_status: ChampionStatusDto, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return champion_status["region"], champion_status[identifier]


def for_champion_status_list_dto(champion_status_list: ChampionStatusListDto) -> str:
    return champion_status_list["region"]


########################
# Champion Mastery API #
########################


def for_champion_mastery_dto(champion_mastery: ChampionMasteryDto) -> Tuple[str, int, int]:
    return champion_mastery["region"], champion_mastery["playerId"], champion_mastery["championId"]


def for_champion_mastery_list_dto(champion_mastery_list: ChampionMasteryListDto) -> Tuple[str, int]:
    return champion_mastery_list["region"], champion_mastery_list["playerId"]


def for_champion_mastery_score_dto(champion_mastery_score: ChampionMasteryScoreDto) -> Tuple[str, int]:
    return champion_mastery_score["region"], champion_mastery_score["summonerId"]


##############
# League API #
##############


def for_league_list_dto(league_list: LeagueListDto) -> Tuple[str, str, str, str]:
    return league_list["region"], league_list["queue"], league_list["tier"], league_list["name"]


def for_league_positions_dto(league_positions: LeaguePositionsDto) -> Tuple[str, int]:
    return league_positions["region"], league_positions["summonerId"]


###################
# Static Data API #
###################


# Champion

def for_champion_dto(champion: ChampionDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return champion["region"], champion["version"], champion["locale"], _hash_included_data(champion["includedData"]), champion[identifier]


def for_champion_list_dto(champion_list: ChampionListDto) -> Tuple[str, str, str, int]:
    return champion_list["region"], champion_list["version"], champion_list["locale"], _hash_included_data(champion_list["includedData"])


# Item

def for_item_dto(item: ItemDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return item["region"], item["version"], item["locale"], _hash_included_data(item["includedData"]), item[identifier]


def for_item_list_dto(item_list: ItemListDto) -> Tuple[str, str, str, int]:
    return item_list["region"], item_list["version"], item_list["locale"], _hash_included_data(item_list["includedData"])


# Language

def for_language_strings_dto(language_strings: LanguageStringsDto) -> Tuple[str, str, str]:
    return language_strings["region"], language_strings["version"], language_strings["locale"]


def for_languages_dto(languages: LanguagesDto) -> str:
    return languages["region"]


# Map

def for_map_dto(map: MapDto, identifier: str = "mapId") -> Tuple[str, str, str, Union[str, int]]:
    return map["region"], map["version"], map["locale"], map[identifier]


def for_map_list_dto(map_list: MapListDto) -> Tuple[str, str, str]:
    return map_list["region"], map_list["version"], map_list["locale"]


# Mastery

def for_mastery_dto(mastery: MasteryDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return mastery["region"], mastery["version"], mastery["locale"], _hash_included_data(mastery["includedData"]), mastery[identifier]


def for_mastery_list_dto(mastery_list: MasteryListDto) -> Tuple[str, str, str, int]:
    return mastery_list["region"], mastery_list["version"], mastery_list["locale"], _hash_included_data(mastery_list["includedData"])


# Profile Icon

def for_profile_icon_data_dto(profile_icon_data: ProfileIconDataDto) -> Tuple[str, str, str]:
    return profile_icon_data["region"], profile_icon_data["version"], profile_icon_data["locale"]


def for_profile_icon_dto(profile_icon: ProfileIconDetailsDto) -> Tuple[str, str, str, int]:
    return profile_icon["region"], profile_icon["version"], profile_icon["locale"], profile_icon["id"]


# Realm

def for_realm_dto(realm: RealmDto) -> str:
    return realm["region"]


# Rune

def for_rune_dto(rune: RuneDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return rune["region"], rune["version"], rune["locale"], _hash_included_data(rune["includedData"]), rune[identifier]


def for_rune_list_dto(rune_list: RuneListDto) -> Tuple[str, str, str, int]:
    return rune_list["region"], rune_list["version"], rune_list["locale"], _hash_included_data(rune_list["includedData"])


# Summoner Spell

def for_summoner_spell_dto(summoner_spell: SummonerSpellDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return summoner_spell["region"], summoner_spell["version"], summoner_spell["locale"], _hash_included_data(summoner_spell["includedData"]), summoner_spell[identifier]


def for_summoner_spell_list_dto(summoner_spell_list: SummonerSpellListDto) -> Tuple[str, str, str, int]:
    return summoner_spell_list["region"], summoner_spell_list["version"], summoner_spell_list["locale"], _hash_included_data(summoner_spell_list["includedData"])


# Version

def for_version_list_dto(version_list: VersionListDto) -> str:
    return version_list["region"]


##############
# Status API #
##############


def for_shard_status_dto(shard_status: ShardStatusDto) -> str:
    return shard_status["region"]


#################
# Masteries API #
#################


def for_mastery_page_dto(mastery_page: MasteryPageDto) -> Tuple[str, int, int]:
    return mastery_page["region"], mastery_page["summonerId"], mastery_page["id"]


def for_mastery_pages_dto(mastery_pages: MasteryPagesDto) -> Tuple[str, int]:
    return mastery_pages["region"], mastery_pages["summonerId"]


#############
# Match API #
#############


def for_match_dto(match: MatchDto) -> Tuple[str, int]:
    return match["region"], match["gameId"]


def for_match_reference_dto(match_reference: MatchReferenceDto) -> Tuple[str, int]:
    return match_reference["region"], match_reference["gameId"]


def for_match_timeline_dto(match_timeline: MatchTimelineDto) -> Tuple[str, int]:
    return match_timeline["region"], match_timeline["matchId"]


#############
# Runes API #
#############


def for_rune_page_dto(rune_page: RunePageDto) -> Tuple[str, int, int]:
    return rune_page["region"], rune_page["summonerId"], rune_page["id"]


def for_rune_pages_dto(rune_pages: RunePagesDto) -> Tuple[str, int]:
    return rune_pages["region"], rune_pages["summonerId"]


#################
# Spectator API #
#################


def for_current_game_info_dto(current_game_info: CurrentGameInfoDto) -> Tuple[str, int]:
    return current_game_info["region"], current_game_info["gameId"]


def for_featured_games_dto(featured_games: FeaturedGamesDto) -> str:
    return featured_games["region"]


################
# Summoner API #
################


def for_summoner_dto(summoner: SummonerDto, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return summoner["region"], summoner[identifier]


########
# Core #
########


##########################################################
# Champion API (Covered by Static Data Champion in core) #
##########################################################


########################
# Champion Mastery API #
########################


def for_champion_mastery(champion_mastery: ChampionMastery, summoner_identifier: str = "id", champion_identifier: str = "id") -> Tuple[str, Union[int, str], Union[int, str]]:
    return champion_mastery.region.value, getattr(champion_mastery.summoner, summoner_identifier), getattr(champion_mastery.champion, champion_identifier)


##############
# League API #
##############


def for_league_summoner(league_summoner: LeagueSummoner, summoner_identifier: str = "id") -> Tuple[str, str, Union[int, str]]:
    return league_summoner.region.value, league_summoner.queue.value, getattr(league_summoner.summoner, summoner_identifier)


###################
# Static Data API #
###################


# Champion

def for_champion(champion: Champion, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return champion.region.value, champion.version, champion.locale, _hash_included_data(champion.included_data), getattr(champion, identifier)


# Item

def for_item(item: Item, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return item.region.value, item.version, item.locale, _hash_included_data(item.included_data), getattr(item, identifier)


# Language TODO


# Map

def for_map(map: Map, identifier: str = "id") -> Tuple[str, str, str, Union[str, int]]:
    return map.region.value, map.version, map.locale, getattr(map, identifier)


# Mastery

def for_mastery(mastery: Mastery, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return mastery.region.value, mastery.version, mastery.locale, _hash_included_data(mastery.included_data), getattr(mastery, identifier)


# Profile Icon TODO


# Realm TODO


# Rune

def for_rune(rune: Rune, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return rune.region.value, rune.version, rune.locale, _hash_included_data(rune.included_data), getattr(rune, identifier)


# Summoner Spell

def for_summoner_spell(summoner_spell: SummonerSpell, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return summoner_spell.region.value, summoner_spell.version, summoner_spell.locale, _hash_included_data(summoner_spell.included_data), getattr(summoner_spell, identifier)


##############
# Status API TODO #
##############


#################
# Masteries API #
#################


def for_mastery_page(mastery_page: MasteryPage, summoner_identifier: str = "id") -> Tuple[str, Union[int, str], int]:
    return mastery_page.region.value, getattr(mastery_page.summoner, summoner_identifier), mastery_page.id


#############
# Match API #
#############


def for_match(match: Match) -> Tuple[str, int]:
    return match.region.value, match.id


#############
# Runes API #
#############


def for_rune_page(rune_page: RunePage, summoner_identifier: str = "id") -> Tuple[str, int, int]:
    return rune_page.region.value, getattr(rune_page.summoner, summoner_identifier), rune_page.id


#################
# Spectator API TODO #
#################


################
# Summoner API #
################


def for_summoner(summoner: Summoner, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return summoner.region.value, getattr(summoner, identifier)
