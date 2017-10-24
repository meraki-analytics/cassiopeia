from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, validate_query

from ..data import Platform, Queue
from ..core import Champion, Champions, Rune, Mastery, Item, Map, SummonerSpell, Realms, ProfileIcon, ProfileIcons, LanguageStrings, Locales, Versions, Masteries, Runes, SummonerSpells, Maps, Items, Summoner, ChampionMastery, ChampionMasteries, RunePages, MasteryPages, Match, MatchHistory, CurrentMatch, FeaturedMatches, ShardStatus, ChallengerLeague, MasterLeague, League, LeagueEntries
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

    @staticmethod
    def create_ghost(cls: Type[T], kwargs) -> T:
        return type.__call__(cls, **kwargs)

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
        can_have("beginIndex").with_default(0).also. \
        can_have("endIndex").with_default(100).also. \
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
        return UnloadedGhostStore.create_ghost(Champion, query)

    @get.register(Champions)
    @validate_query(_validate_get_champions_query, convert_region_to_platform)
    def get_champions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Champions:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        query.pop("dataById")
        return UnloadedGhostStore.create_ghost(Champions, query)

    @get.register(Rune)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Rune:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Rune, query)

    @get.register(Mastery)
    @validate_query(_validate_get_mastery_query, convert_region_to_platform)
    def get_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Mastery:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Mastery, query)

    @get.register(Item)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Item:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Item, query)

    @get.register(Map)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Map:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Map, query)

    @get.register(SummonerSpell)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(SummonerSpell, query)

    @get.register(Realms)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Realms:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Realms, query)

    @get.register(ProfileIcon)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(ProfileIcon, query)

    @get.register(ProfileIcons)
    @validate_query(_validate_get_profile_icons_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(ProfileIcons, query)

    @get.register(LanguageStrings)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(LanguageStrings, query)

    @get.register(Locales)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_locales(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Locales:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Locales, query)

    @get.register(Versions)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Versions:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Versions, query)

    @get.register(Runes)
    @validate_query(_validate_get_runes_query, convert_region_to_platform)
    def get_runes(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Runes:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Runes, query)

    @get.register(Masteries)
    @validate_query(_validate_get_masteries_query, convert_region_to_platform)
    def get_masteries(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Masteries:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Masteries, query)

    @get.register(SummonerSpells)
    @validate_query(_validate_get_summoner_spells_query, convert_region_to_platform)
    def get_summoner_spells(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpells:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(SummonerSpells, query)

    @get.register(Maps)
    @validate_query(_validate_get_maps_query, convert_region_to_platform)
    def get_maps(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Maps:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Maps, query)

    @get.register(Items)
    @validate_query(_validate_get_items_query, convert_region_to_platform)
    def get_items(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Items:
        query["region"] = query.pop("platform").region
        query["included_data"] = query.pop("includedData")
        return UnloadedGhostStore.create_ghost(Items, query)

    @get.register(Summoner)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Summoner:
        query["region"] = query.pop("platform").region
        if "account.id" in query:
            query["account"] = query.pop("account.id")
        return UnloadedGhostStore.create_ghost(Summoner, query)

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
        return UnloadedGhostStore.create_ghost(ChampionMastery, query)

    @get.register(ChampionMasteries)
    @validate_query(_validate_get_champion_masteries_query, convert_region_to_platform)
    def get_champion_masteries(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteries:
        query["region"] = query.pop("platform").region
        if "summoner.id" in query:
            query["summoner"] = query.pop("summoner.id")
        if "summoner.name" in query:
            query["summoner"] = query.pop("summoner.name")
        if "summoner.account.id" in query:
            query["_account_id"] = query.pop("summoner.account.id")
        return UnloadedGhostStore.create_ghost(ChampionMasteries, query)

    @get.register(RunePages)
    @validate_query(_validate_get_rune_pages_query, convert_region_to_platform)
    def get_rune_pages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RunePages:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return UnloadedGhostStore.create_ghost(RunePages, query)

    @get.register(MasteryPages)
    @validate_query(_validate_get_mastery_pages_query, convert_region_to_platform)
    def get_mastery_pages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasteryPages:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return UnloadedGhostStore.create_ghost(MasteryPages, query)

    @get.register(Match)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Match:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Match, query)

    @get.register(Timeline)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Timeline:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(Timeline, query)

    @get.register(MatchHistory)
    @validate_query(_validate_get_match_history_query, convert_region_to_platform)
    def get_match_history(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchHistory:
        query["region"] = query.pop("platform").region
        query["account_id"] = query.pop("account.id")
        query["begin_index"] = query.pop("beginIndex")
        query["end_index"] = query.pop("endIndex")
        if "beginTime" in query:
            query["begin_time"] = query.pop("beginTime")
        if "endTime" in query:
            query["end_time"] = query.pop("endTime")
        if "champion.ids" in query:
            query["champions"] = query.pop("champion.ids")
        return UnloadedGhostStore.create_ghost(MatchHistory, query)

    @get.register(CurrentMatch)
    @validate_query(_validate_get_current_match_query, convert_region_to_platform)
    def get_current_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentMatch:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return UnloadedGhostStore.create_ghost(CurrentMatch, query)

    @get.register(FeaturedMatches)
    @validate_query(_validate_get_featured_matches_query, convert_region_to_platform)
    def get_featured_matches(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> FeaturedMatches:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(FeaturedMatches, query)

    @get.register(ShardStatus)
    @validate_query(_validate_get_shard_status_query, convert_region_to_platform)
    def get_shard_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(ShardStatus, query)

    @get.register(ChallengerLeague)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeague:
        UnloadedGhostStore._validate_get_challenger_league_query(query)
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(ChallengerLeague, query)

    @get.register(MasterLeague)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        query["region"] = query.pop("platform").region
        return UnloadedGhostStore.create_ghost(MasterLeague, query)

    @get.register(League)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_leagues(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> League:
        query["region"] = query.pop("platform").region
        query["id"] = query.pop("id")
        return UnloadedGhostStore.create_ghost(League, query)

    @get.register(LeagueEntries)
    @validate_query(_validate_get_league_entries_query, convert_region_to_platform)
    def get_league_entries(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueEntries:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return UnloadedGhostStore.create_ghost(LeagueEntries, query)
