from typing import Tuple, Set, Union, MutableMapping, Any, Mapping

from datapipelines import Query, PipelineContext

from ..data import Region, Platform, Queue, Tier

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


def _get_default_version(query: Mapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: Mapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


def convert_region_to_platform(query: MutableMapping[str, Any]) -> None:
    try:
        region = query["region"]
        if isinstance(region, str):
            region = Region(region)
        if isinstance(region, Region):
            query["platform"] = region.platform
    except KeyError:
        pass


#######
# DTO #
#######


################
# Champion API #
################


validate_champion_status_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("id").as_(int)


def for_champion_status_dto(champion_status: ChampionStatusDto) -> Tuple[str, int]:
    return champion_status["platform"], champion_status["id"]


def for_champion_status_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["id"]


validate_champion_status_list_dto_query = Query. \
    has("platform").as_(Platform)


def for_champion_status_list_dto(champion_status_list: ChampionStatusListDto) -> str:
    return champion_status_list["platform"]


def for_champion_status_list_dto_query(query: Query) -> str:
    return query["platform"].value


########################
# Champion Mastery API #
########################


validate_champion_mastery_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int).also. \
    has("championId").as_(int)


def for_champion_mastery_dto(champion_mastery: ChampionMasteryDto) -> Tuple[str, int, int]:
    return champion_mastery["platform"], champion_mastery["summonerId"], champion_mastery["championId"]


def for_champion_mastery_dto_query(query: Query) -> Tuple[str, int, int]:
    return query["platform"].value, query["summonerId"], query["championId"]


validate_champion_mastery_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int)


def for_champion_mastery_list_dto(champion_mastery_list: ChampionMasteryListDto) -> Tuple[str, int]:
    return champion_mastery_list["platform"], champion_mastery_list["summonerId"]


def for_champion_mastery_list_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["summonerId"]


validate_champion_mastery_score_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int)


def for_champion_mastery_score_dto(champion_mastery_score: ChampionMasteryScoreDto) -> Tuple[str, int]:
    return champion_mastery_score["platform"], champion_mastery_score["summonerId"]


def for_champion_mastery_score_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["summonerId"]


##############
# League API #
##############


validate_league_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("queue").as_(Queue).also. \
    has("tier").as_(Tier).also. \
    has("name").as_(str)


def for_league_list_dto(league_list: LeagueListDto) -> Tuple[str, str, str, str]:
    return league_list["platform"], league_list["queue"], league_list["tier"], league_list["name"]


def for_league_list_dto_query(query: Query) -> Tuple[str, str, str, str]:
    return query["platform"].value, query["queue"].value, query["tier"].value, query["name"]


validate_league_positions_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int)


def for_league_positions_dto(league_positions: LeaguePositionsDto) -> Tuple[str, int]:
    return league_positions["platform"], league_positions["summonerId"]


def for_league_positions_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["summonerId"]


###################
# Static Data API #
###################


# Champion

validate_champion_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_champion_dto(champion: ChampionDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return champion["platform"], champion["version"], champion["locale"], _hash_included_data(champion["includedData"]), champion[identifier]


def for_champion_dto_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"]), query[identifier]


validate_champion_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"})


def for_champion_list_dto(champion_list: ChampionListDto) -> Tuple[str, str, str, int]:
    return champion_list["platform"], champion_list["version"], champion_list["locale"], _hash_included_data(champion_list["includedData"])


def for_champion_list_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"])


# Item


validate_item_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_item_dto(item: ItemDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return item["platform"], item["version"], item["locale"], _hash_included_data(item["includedData"]), item[identifier]


def for_item_dto_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"]), query[identifier]


validate_item_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"})


def for_item_list_dto(item_list: ItemListDto) -> Tuple[str, str, str, int]:
    return item_list["platform"], item_list["version"], item_list["locale"], _hash_included_data(item_list["includedData"])


def for_item_list_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"])


# Language


validate_language_strings_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str)


def for_language_strings_dto(language_strings: LanguageStringsDto) -> Tuple[str, str, str]:
    return language_strings["platform"], language_strings["version"], language_strings["locale"]


def for_language_strings_dto_query(query: Query) -> Tuple[str, str, str]:
    return query["platform"].value, query["version"], query["locale"]


validate_languages_dto_query = Query. \
    has("platform").as_(Platform)


def for_languages_dto(languages: LanguagesDto) -> str:
    return languages["platform"]


def for_languages_dto_query(query: Query) -> str:
    return query["platform"].value


# Map


validate_map_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    has("mapId").as_(int).or_("mapName").as_(str)


def for_map_dto(map: MapDto, identifier: str = "mapId") -> Tuple[str, str, str, Union[int, str]]:
    return map["platform"], map["version"], map["locale"], map[identifier]


def for_map_dto_query(query: Query) -> Tuple[str, str, str, Union[int, str]]:
    identifier = "mapId" if "mapId" in query else "mapName"
    return query["platform"].value, query["version"], query["locale"], query[identifier]


validate_map_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str)


def for_map_list_dto(map_list: MapListDto) -> Tuple[str, str, str]:
    return map_list["platform"], map_list["version"], map_list["locale"]


def for_map_list_dto_query(query: Query) -> Tuple[str, str, str]:
    return query["platform"].value, query["version"], query["locale"]


# Mastery

validate_mastery_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_mastery_dto(mastery: MasteryDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return mastery["platform"], mastery["version"], mastery["locale"], _hash_included_data(mastery["includedData"]), mastery[identifier]


def for_mastery_dto_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"], query["version"], query["locale"], _hash_included_data(query["includedData"]), query[identifier]


validate_mastery_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"})


def for_mastery_list_dto(mastery_list: MasteryListDto) -> Tuple[str, str, str, int]:
    return mastery_list["platform"], mastery_list["version"], mastery_list["locale"], _hash_included_data(mastery_list["includedData"])


def for_mastery_list_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"], query["version"], query["locale"], _hash_included_data(query["includedData"])


# Profile Icon


validate_profile_icon_data_dto_query = Query. \
    has("platform").as_(Platform). \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str)


def for_profile_icon_data_dto(profile_icon_data: ProfileIconDataDto) -> Tuple[str, str, str]:
    return profile_icon_data["platform"], profile_icon_data["version"], profile_icon_data["locale"]


def for_profile_icon_data_dto_query(query: Query) -> Tuple[str, str, str]:
    return query["platform"].value, query["version"], query["locale"]


validate_profile_icon_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    has("id").as_(int)


def for_profile_icon_dto(profile_icon: ProfileIconDetailsDto) -> Tuple[str, str, str, int]:
    return profile_icon["platform"], profile_icon["version"], profile_icon["locale"], profile_icon["id"]


def for_profile_icon_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], query["id"]


# Realm


validate_realm_dto_query = Query. \
    has("platform").as_(Platform)


def for_realm_dto(realm: RealmDto) -> str:
    return realm["platform"]


def for_realm_dto_query(query: Query) -> str:
    return query["platform"].value


# Rune


validate_rune_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_rune_dto(rune: RuneDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return rune["platform"], rune["version"], rune["locale"], _hash_included_data(rune["includedData"]), rune[identifier]


def for_rune_dto_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"]), query[identifier]


validate_rune_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"})


def for_rune_list_dto(rune_list: RuneListDto) -> Tuple[str, str, str, int]:
    return rune_list["platform"], rune_list["version"], rune_list["locale"], _hash_included_data(rune_list["includedData"])


def for_rune_list_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"])


# Summoner Spell


validate_summoner_spell_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_summoner_spell_dto(summoner_spell: SummonerSpellDto, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return summoner_spell["platform"], summoner_spell["version"], summoner_spell["locale"], _hash_included_data(summoner_spell["includedData"]), summoner_spell[identifier]


def for_summoner_spell_dto_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"]), query[identifier]


validate_summoner_spell_list_dto_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("includedData").with_default({"all"})


def for_summoner_spell_list_dto(summoner_spell_list: SummonerSpellListDto) -> Tuple[str, str, str, int]:
    return summoner_spell_list["platform"], summoner_spell_list["version"], summoner_spell_list["locale"], _hash_included_data(summoner_spell_list["includedData"])


def for_summoner_spell_list_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["includedData"])


# Version


validate_version_list_dto_query = Query. \
    has("platform").as_(Platform)


def for_version_list_dto(version_list: VersionListDto) -> str:
    return version_list["platform"]


def for_version_list_dto_query(version_list: VersionListDto) -> str:
    return version_list["platform"].value


##############
# Status API #
##############


validate_shard_status_dto_query = Query. \
    has("platform").as_(Platform)


def for_shard_status_dto(shard_status: ShardStatusDto) -> str:
    return shard_status["platform"]


def for_shard_status_dto_query(shard_status: ShardStatusDto) -> str:
    return shard_status["platform"].value


#################
# Masteries API #
#################


validate_mastery_page_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").also. \
    has("id").as_(int)


def for_mastery_page_dto(mastery_page: MasteryPageDto) -> Tuple[str, int, int]:
    return mastery_page["platform"], mastery_page["summonerId"], mastery_page["id"]


def for_mastery_page_dto_query(query: Query) -> Tuple[str, int, int]:
    return query["platform"].value, query["summonerId"], query["id"]


validate_mastery_pages_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int)


def for_mastery_pages_dto(mastery_pages: MasteryPagesDto) -> Tuple[str, int]:
    return mastery_pages["platform"], mastery_pages["summonerId"]


def for_mastery_pages_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["summonerId"]


#############
# Match API #
#############


validate_match_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("gameId").as_(int)


def for_match_dto(match: MatchDto) -> Tuple[str, int]:
    return match["platform"], match["gameId"]


def for_match_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["gameId"]


validate_match_reference_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("gameId").as_(int)


def for_match_reference_dto(match_reference: MatchReferenceDto) -> Tuple[str, int]:
    return match_reference["platform"], match_reference["gameId"]


def for_match_reference_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["gameId"]


validate_match_timeline_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("matchId").as_(int)


def for_match_timeline_dto(match_timeline: MatchTimelineDto) -> Tuple[str, int]:
    return match_timeline["platform"], match_timeline["matchId"]


def for_match_timeline_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["matchId"]


#############
# Runes API #
#############


validate_rune_page_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int).also. \
    has("id").as_(int)


def for_rune_page_dto(rune_page: RunePageDto) -> Tuple[str, int, int]:
    return rune_page["platform"], rune_page["summonerId"], rune_page["id"]


def for_rune_page_dto_query(query: Query) -> Tuple[str, int, int]:
    return query["platform"].value, query["summonerId"], query["id"]


validate_rune_pages_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("summonerId").as_(int)


def for_rune_pages_dto(rune_pages: RunePagesDto) -> Tuple[str, int]:
    return rune_pages["platform"], rune_pages["summonerId"]


def for_rune_pages_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["summonerId"]


#################
# Spectator API #
#################


validate_current_game_info_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("gameId").as_(int)


def for_current_game_info_dto(current_game_info: CurrentGameInfoDto) -> Tuple[str, int]:
    return current_game_info["platform"], current_game_info["gameId"]


def for_current_game_info_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["gameId"]


validate_features_game_dto_query = Query. \
    has("platform").as_(Platform)


def for_featured_games_dto(featured_games: FeaturedGamesDto) -> str:
    return featured_games["platform"]


def for_featured_games_dto_query(query: Query) -> str:
    return query["platform"].value


################
# Summoner API #
################


validate_summoner_dto_query = Query. \
    has("platform").as_(Platform).also. \
    has("id").as_(int).or_("accountId").as_(int).or_("name").as_(str)


def for_summoner_dto(summoner: SummonerDto, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return summoner["platform"], summoner[identifier]


def for_summoner_dto_query(query: Query) -> Tuple[str, Union[int, str]]:
    if "id" in query:
        identifier = "id"
    elif "accountId" in query:
        identifier = "accountId"
    else:
        identifier = "name"
    return query["platform"].value, query[identifier]


########
# Core #
########


##########################################################
# Champion API (Covered by Static Data Champion in core) #
##########################################################


########################
# Champion Mastery API #
########################


validate_champion_mastery_query = Query. \
    has("platform").as_(Platform).also. \
    has("summoner.id").as_(int).or_("summoner.account_id").as_(int).or_("summoner.name").as_(str).also. \
    has("champion.id").as_(int).or_("champion.name").as_(str)


def for_champion_mastery(champion_mastery: ChampionMastery, summoner_identifier: str = "id", champion_identifier: str = "id") -> Tuple[str, Union[int, str], Union[int, str]]:
    return champion_mastery.platform.value, getattr(champion_mastery.summoner, summoner_identifier), getattr(champion_mastery.champion, champion_identifier)


def for_champion_mastery_query(query: Query) -> Tuple[str, Union[int, str], Union[int, str]]:
    if "summoner.id" in query:
        summoner_identifier = "id"
    elif "summoner.account_id" in query:
        summoner_identifier = "account_id"
    else:
        summoner_identifier = "name"

    champion_identifier = "champion.id" if "champion.id" in query else "champion.name"

    return query["platform"].value, query[summoner_identifier], query[champion_identifier]


##############
# League API #
##############


validate_league_summoner_query = Query. \
    has("platform").as_(Platform).also. \
    has("queue").as_(Queue).also. \
    has("summoner.id").as_(int).or_("summoner.account_id").as_(int).or_("summoner.name").as_(str)


def for_league_summoner(league_summoner: LeagueSummoner, summoner_identifier: str = "id") -> Tuple[str, str, Union[int, str]]:
    return league_summoner.platform.value, league_summoner.queue.value, getattr(league_summoner.summoner, summoner_identifier)


def for_league_summoner_query(query: Query) -> Tuple[str, str, Union[int, str]]:
    if "summoner.id" in query:
        summoner_identifier = "id"
    elif "summoner.account_id" in query:
        summoner_identifier = "account_id"
    else:
        summoner_identifier = "name"
    return query["platform"].value, query["queue"].value, query[summoner_identifier]


###################
# Static Data API #
###################


# Champion

validate_champion_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("included_data").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_champion(champion: Champion, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return champion.platform.value, champion.version, champion.locale, _hash_included_data(champion.included_data), getattr(champion, identifier)


def for_champion_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["included_data"]), query[identifier]


# Item

validate_item_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("included_data").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_item(item: Item, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return item.platform.value, item.version, item.locale, _hash_included_data(item.included_data), getattr(item, identifier)


def for_item_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["included_data"]), query[identifier]


# Language TODO


# Map

validate_map_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    has("id").as_(int).or_("name").as_(str)


def for_map(map: Map, identifier: str = "id") -> Tuple[str, str, str, Union[str, int]]:
    return map.platform.value, map.version, map.locale, getattr(map, identifier)


def for_map_query(query: Query) -> Tuple[str, str, str, Union[str, int]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], query[identifier]


# Mastery

validate_mastery_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("included_data").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_mastery(mastery: Mastery, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return mastery.platform.value, mastery.version, mastery.locale, _hash_included_data(mastery.included_data), getattr(mastery, identifier)


def for_mastery_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["included_data"]), query[identifier]


# Profile Icon TODO


# Realm TODO


# Rune

validate_rune_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("included_data").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_rune(rune: Rune, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return rune.platform.value, rune.version, rune.locale, _hash_included_data(rune.included_data), getattr(rune, identifier)


def for_rune_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["included_data"]), query[identifier]


# Summoner Spell

validate_summoner_spell_query = Query. \
    has("platform").as_(Platform).also. \
    can_have("version").with_default(_get_default_version, supplies_type=str).also. \
    can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
    can_have("included_data").with_default({"all"}).also. \
    has("id").as_(int).or_("name").as_(str)


def for_summoner_spell(summoner_spell: SummonerSpell, identifier: str = "id") -> Tuple[str, str, str, int, Union[int, str]]:
    return summoner_spell.platform.value, summoner_spell.version, summoner_spell.locale, _hash_included_data(summoner_spell.included_data), getattr(summoner_spell, identifier)


def for_summoner_spell_query(query: Query) -> Tuple[str, str, str, int, Union[int, str]]:
    identifier = "id" if "id" in query else "name"
    return query["platform"].value, query["version"], query["locale"], _hash_included_data(query["included_data"]), query[identifier]


##############
# Status API TODO #
##############


#################
# Masteries API #
#################


validate_mastery_page_query = Query. \
    has("platform").as_(Platform).also. \
    has("summoner.id").as_(int).or_("summoner.account_id").as_(int).or_("summoner.name").as_(str).also. \
    has("id").as_(int)


def for_mastery_page(mastery_page: MasteryPage, summoner_identifier: str = "id") -> Tuple[str, Union[int, str], int]:
    return mastery_page.platform.value, getattr(mastery_page.summoner, summoner_identifier), mastery_page.id


def for_mastery_page_query(query: Query) -> Tuple[str, Union[int, str], int]:
    if "summoner.id" in query:
        summoner_identifier = "id"
    elif "summoner.account_id" in query:
        summoner_identifier = "account_id"
    else:
        summoner_identifier = "name"
    return query["platform"].value, query[summoner_identifier], query["id"]


#############
# Match API #
#############


validate_match_query = Query. \
    has("platform").as_(Platform). \
    has("id").as_(int)


def for_match(match: Match) -> Tuple[str, int]:
    return match.platform.value, match.id


def for_match_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["id"]


#############
# Runes API #
#############


validate_rune_page_query = Query. \
    has("platform").as_(Platform).also. \
    has("summoner.id").as_(int).or_("summoner.account_id").as_(int).or_("summoner.name").as_(str).also. \
    has("id").as_(int)


def for_rune_page(rune_page: RunePage, summoner_identifier: str = "id") -> Tuple[str, int, int]:
    return rune_page.platform.value, getattr(rune_page.summoner, summoner_identifier), rune_page.id


def for_rune_page_query(query: Query) -> Tuple[str, Union[int, str], int]:
    if "summoner.id" in query:
        summoner_identifier = "id"
    elif "summoner.account_id" in query:
        summoner_identifier = "account_id"
    else:
        summoner_identifier = "name"
    return query["platform"].value, query[summoner_identifier], query["id"]


#################
# Spectator API TODO #
#################


################
# Summoner API #
################


validate_summoner_query = Query. \
    has("platform").as_(Platform).also. \
    has("id").as_(int).or_("account_id").as_(int).or_("name").as_(str)


def for_summoner(summoner: Summoner, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return summoner.platform.value, getattr(summoner, identifier)


def for_summoner_query(query: Query) -> Tuple[str, Union[int, str]]:
    if "id" in query:
        identifier = "id"
    elif "account_id" in query:
        identifier = "account_id"
    else:
        identifier = "name"
    return query["platform"].value, query[identifier]
