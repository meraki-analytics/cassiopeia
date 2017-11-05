from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, validate_query

from ..data import Platform, Queue
from ..core import Champion, Rune, Mastery, Item, Map, SummonerSpell, Realms, ProfileIcon, LanguageStrings, Summoner, ChampionMastery, Match, CurrentMatch, ShardStatus, ChallengerLeague, MasterLeague, League
from ..core.match import Timeline
from .riotapi.staticdata import _get_latest_version, _get_default_locale
from .uniquekeys import convert_region_to_platform

T = TypeVar("T")


class UnloadedGhostStore(DataSource):
    def __init__(self):
        super().__init__()

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    _validate_get_champion_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    _validate_get_champions_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"}).also. \
        can_have("dataById").with_default(True)

    _validate_get_mastery_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_masteries_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_rune_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_runes_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_item_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_items_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_map_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_maps_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_summoner_spell_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_summoner_spells_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_languages_query = Query. \
        has("platform").as_(Platform)

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_profile_icon_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_profile_icons_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").also. \
        has("champion.id").as_(int)

    _validate_get_champion_masteries_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    _validate_get_league_entries_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_league_query = Query. \
        has("id").as_(str).also. \
        has("platform").as_(Platform)

    _validate_get_challenger_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    _validate_get_master_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    _validate_get_mastery_pages_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_rune_pages_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_current_match_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    _validate_get_featured_matches_query = Query. \
        has("platform").as_(Platform)

    _validate_get_match_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_match_history_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    _validate_get_timeline_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_shard_status_query = Query. \
        has("platform").as_(Platform)

    _validate_get_summoner_query = Query. \
        has("id").as_(int). \
        or_("account.id").as_(int). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(Champion)
    @validate_query(_validate_get_champion_query, convert_region_to_platform)
    def get_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Champion:
        query["region"] = query.pop("platform").region
        return Champion._construct_normally(**query)

    @get.register(Rune)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Rune:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return Rune._construct_normally(**query)

    @get.register(Mastery)
    @validate_query(_validate_get_mastery_query, convert_region_to_platform)
    def get_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Mastery:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return Mastery._construct_normally(**query)

    @get.register(Item)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Item:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return Item._construct_normally(**query)

    @get.register(Map)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Map:
        query["region"] = query.pop("platform").region
        return Map._construct_normally(**query)

    @get.register(SummonerSpell)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return SummonerSpell._construct_normally(**query)

    @get.register(Realms)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Realms:
        query["region"] = query.pop("platform").region
        return Realms._construct_normally(**query)

    @get.register(ProfileIcon)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        query["region"] = query.pop("platform").region
        return ProfileIcon._construct_normally(**query)

    @get.register(LanguageStrings)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        query["region"] = query.pop("platform").region
        return LanguageStrings._construct_normally(**query)

    @get.register(Summoner)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Summoner:
        query["region"] = query.pop("platform").region
        if "account.id" in query:
            query["account"] = query.pop("account.id")
        return Summoner._construct_normally(**query)

    @get.register(ChampionMastery)
    @validate_query(_validate_get_champion_mastery_query, convert_region_to_platform)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMastery:
        query["region"] = query.pop("platform").region
        if "summoner.id" in query:
            query["summoner"] = query.pop("summoner.id")
        if "summoner.name" in query:
            query["summoner"] = query.pop("summoner.name")
        if "summoner.account.id" in query:
            query["_account_id"] = query.pop("summoner.account.id")
        if "champion.id" in query:
            query["champion"] = query.pop("champion.id")
        if "champion.id" in query:
            query["champion"] = query.pop("champion.name")
        return ChampionMastery._construct_normally(**query)

    @get.register(Match)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Match:
        query["region"] = query.pop("platform").region
        return Match._construct_normally(**query)

    @get.register(Timeline)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Timeline:
        query["region"] = query.pop("platform").region
        return Timeline._construct_normally(**query)

    @get.register(CurrentMatch)
    @validate_query(_validate_get_current_match_query, convert_region_to_platform)
    def get_current_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentMatch:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return CurrentMatch._construct_normally(**query)

    @get.register(ShardStatus)
    @validate_query(_validate_get_shard_status_query, convert_region_to_platform)
    def get_shard_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        query["region"] = query.pop("platform").region
        return ShardStatus._construct_normally(**query)

    @get.register(ChallengerLeague)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeague:
        UnloadedGhostStore._validate_get_challenger_league_query(query)
        query["region"] = query.pop("platform").region
        return ChallengerLeague._construct_normally(**query)

    @get.register(MasterLeague)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        query["region"] = query.pop("platform").region
        return MasterLeague._construct_normally(**query)

    @get.register(League)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> League:
        query["region"] = query.pop("platform").region
        query["id"] = query.pop("id")
        return League._construct_normally(**query)
