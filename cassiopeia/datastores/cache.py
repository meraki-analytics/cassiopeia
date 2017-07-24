from typing import Type, Mapping, Any, Iterable, TypeVar, Tuple, Callable, Generator

from datapipelines import DataSource, DataSink, PipelineContext, validate_query, NotFoundError
from merakicommons.cache import Cache as CommonsCache

from . import uniquekeys
from ..core.championmastery import ChampionMastery
from ..core.league import LeagueSummoner
from ..core.staticdata import Champion, Mastery, Rune, Item, SummonerSpell, Map, Realms, ProfileIcon, Languages, LanguageStrings, Versions, SummonerSpells, Items
from ..core.masterypage import MasteryPage
from ..core.match import Match
from ..core.runepage import RunePage
from ..core.summoner import Summoner
from ..core.status import ShardStatus
from ..core.spectator import CurrentMatch, FeaturedMatches


T = TypeVar("T")


class Cache(DataSource, DataSink):
    def __init__(self, expiration: Mapping[type, float] = None) -> None:
        self._cache = CommonsCache()
        self._expiration = dict(expiration) if expiration is not None else {}

    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    def _get(self, query: Mapping[str, Any], key_function: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None):
        key = key_function(query)
        try:
            return self._cache.get(key)
        except KeyError as e:
            raise NotFoundError from e

    def _get_many(self, query: Mapping[str, Any], key_generator: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None):
        for key in key_generator(query):
            try:
                yield self._cache.get(key)
            except KeyError as e:
                raise NotFoundError from e

    @staticmethod
    def _put_many_generator(items: Iterable[T], key_function: Callable[[T], Any], *key_function_arg_lists: tuple) -> Generator[Tuple[Any, T], None, None]:
        for item in items:
            for key_function_args in key_function_arg_lists:
                yield key_function(item, *key_function_args), item

    def _put(self, type: Type[T], item: T, key_function: Callable[[T], Any], *key_function_arg_lists: tuple, context: PipelineContext = None) -> None:
        try:
            expire_seconds = self._expiration[type]
        except KeyError:
            expire_seconds = -1.0

        if not key_function_arg_lists:
            key = key_function(item)
            self._cache.put(key, item, expire_seconds)
        else:
            for key_function_args in key_function_arg_lists:
                key = key_function(item, *key_function_args)
                self._cache.put(key, item, expire_seconds)
        # TODO: Put EXPIRATION into context once cache expiration works

    def _put_many(self, type: Type[T], items: Iterable[T], key_function: Callable[[T], Any], *key_function_arg_lists: tuple, context: PipelineContext = None) -> None:
        try:
            expire_seconds = self._expiration[type]
        except KeyError:
            expire_seconds = -1.0

        for key, item in Cache._put_many_generator(items, key_function, *key_function_arg_lists):
            self._cache.put(key, item, expire_seconds)
        # TODO: Put EXPIRATION into context once cache expiration works

    ########################
    # Champion Mastery API #
    ########################

    @get.register(ChampionMastery)
    @validate_query(uniquekeys.validate_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champion:
        return self._get(query, uniquekeys.for_champion_mastery_query, context)

    @get_many.register(ChampionMastery)
    @validate_query(uniquekeys.validate_many_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_many_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champion, None, None]:
        return self._get_many(query, uniquekeys.for_many_champion_mastery_query, context)

    @put.register(ChampionMastery)
    def put_champion_mastery(self, item: ChampionMastery, context: PipelineContext = None) -> None:
        self._put(ChampionMastery, item, uniquekeys.for_champion_mastery,
            ("id", "id"),
            ("id", "name"),
            ("account.id", "id"),
            ("account.id", "name"),
            ("name", "id"),
            ("name", "name"),
            context=context)

    @put_many.register(ChampionMastery)
    def put_many_champion_mastery(self, items: Iterable[ChampionMastery], context: PipelineContext = None) -> None:
        self._put_many(ChampionMastery, items, uniquekeys.for_champion_mastery,
            ("id", "id"),
            ("id", "name"),
            ("account.id", "id"),
            ("account.id", "name"),
            ("name", "id"),
            ("name", "name"),
            context=context)

    ##############
    # League API #
    ##############

    @get.register(LeagueSummoner)
    @validate_query(uniquekeys.validate_league_summoner_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> LeagueSummoner:
        return self._get(query, uniquekeys.for_champion_mastery_query, context)

    @get_many.register(LeagueSummoner)
    @validate_query(uniquekeys.validate_many_league_summoner_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LeagueSummoner, None, None]:
        return self._get_many(query, uniquekeys.for_many_champion_mastery_query, context)

    @put.register(LeagueSummoner)
    def put_league_summoner(self, item: LeagueSummoner, context: PipelineContext = None) -> None:
        self._put(LeagueSummoner, item, uniquekeys.for_league_summoner, ("id",), ("account.id",), ("name",), context=context)

    @put_many.register(LeagueSummoner)
    def put_many_league_summoner(self, items: Iterable[LeagueSummoner], context: PipelineContext = None) -> None:
        self._put_many(LeagueSummoner, items, uniquekeys.for_league_summoner, ("id",), ("account.id",), ("name",), context=context)

    ###################
    # Static Data API #
    ###################
    
    # Champion

    @get.register(Champion)
    @validate_query(uniquekeys.validate_champion_query, uniquekeys.convert_region_to_platform)
    def get_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champion:
        return self._get(query, uniquekeys.for_champion_query, context)

    @get_many.register(Champion)
    @validate_query(uniquekeys.validate_many_champion_query, uniquekeys.convert_region_to_platform)
    def get_many_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champion, None, None]:
        return self._get_many(query, uniquekeys.for_many_champion_query, context)

    @put.register(Champion)
    def put_champion(self, item: Champion, context: PipelineContext = None) -> None:
        self._put(Champion, item, uniquekeys.for_champion, ("id",), ("name",), context=context)

    @put_many.register(Champion)
    def put_many_champion(self, items: Iterable[Champion], context: PipelineContext = None) -> None:
        self._put_many(Champion, items, uniquekeys.for_champion, ("id",), ("name",), context=context)

    # Item

    @get.register(Item)
    @validate_query(uniquekeys.validate_item_query, uniquekeys.convert_region_to_platform)
    def get_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Item:
        return self._get(query, uniquekeys.for_item_query, context)

    @get_many.register(Item)
    @validate_query(uniquekeys.validate_many_item_query, uniquekeys.convert_region_to_platform)
    def get_many_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Item, None, None]:
        return self._get_many(query, uniquekeys.for_many_item_query, context)

    @put.register(Item)
    def put_item(self, item: Item, context: PipelineContext = None) -> None:
        self._put(Item, item, uniquekeys.for_item, ("id",), ("name",), context=context)

    @put_many.register(Item)
    def put_many_item(self, items: Iterable[Item], context: PipelineContext = None) -> None:
        self._put_many(Item, items, uniquekeys.for_item, ("id",), ("name",), context=context)

    @get.register(Items)
    @validate_query(uniquekeys.validate_items_query, uniquekeys.convert_region_to_platform)
    def get_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Items:
        return self._get(query, uniquekeys.for_items_query, context)

    @get_many.register(Items)
    @validate_query(uniquekeys.validate_many_items_query, uniquekeys.convert_region_to_platform)
    def get_many_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Items, None, None]:
        return self._get_many(query, uniquekeys.for_many_items_query, context)

    @put.register(Items)
    def put_items(self, item: Items, context: PipelineContext = None) -> None:
        self._put(Items, item, uniquekeys.for_items, ("platform",), context=context)

    @put_many.register(Items)
    def put_many_items(self, items: Iterable[Items], context: PipelineContext = None) -> None:
        self._put_many(Items, items, uniquekeys.for_items, ("platform",), context=context)

    # Language

    @get.register(Languages)
    @validate_query(uniquekeys.validate_languages_query, uniquekeys.convert_region_to_platform)
    def get_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Languages:
        return self._get(query, uniquekeys.for_languages_query, context)

    @get_many.register(Languages)
    @validate_query(uniquekeys.validate_many_languages_query, uniquekeys.convert_region_to_platform)
    def get_many_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Languages, None, None]:
        return self._get_many(query, uniquekeys.for_many_languages_query, context)

    @put.register(Languages)
    def put_languages(self, item: Languages, context: PipelineContext = None) -> None:
        self._put(Languages, item, uniquekeys.for_languages, context=context)

    @put_many.register(Languages)
    def put_many_languages(self, items: Iterable[Languages], context: PipelineContext = None) -> None:
        self._put_many(Languages, items, uniquekeys.for_languages, context=context)

    @get.register(LanguageStrings)
    @validate_query(uniquekeys.validate_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        return self._get(query, uniquekeys.for_language_strings_query, context)

    @get_many.register(LanguageStrings)
    @validate_query(uniquekeys.validate_many_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_many_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LanguageStrings, None, None]:
        return self._get_many(query, uniquekeys.for_many_language_strings_query, context)

    @put.register(LanguageStrings)
    def put_language_strings(self, item: LanguageStrings, context: PipelineContext = None) -> None:
        self._put(LanguageStrings, item, uniquekeys.for_language_strings, context=context)

    @put_many.register(LanguageStrings)
    def put_many_language_strings(self, items: Iterable[LanguageStrings], context: PipelineContext = None) -> None:
        self._put_many(LanguageStrings, items, uniquekeys.for_language_strings, context=context)

    # Map

    @get.register(Map)
    @validate_query(uniquekeys.validate_map_query, uniquekeys.convert_region_to_platform)
    def get_map(self, query: Mapping[str, Any], context: PipelineContext = None) -> Map:
        return self._get(query, uniquekeys.for_map_query, context)

    @get_many.register(Map)
    @validate_query(uniquekeys.validate_many_map_query, uniquekeys.convert_region_to_platform)
    def get_many_map(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Map, None, None]:
        return self._get_many(query, uniquekeys.for_many_map_query, context)

    @put.register(Map)
    def put_map(self, item: Map, context: PipelineContext = None) -> None:
        self._put(Map, item, uniquekeys.for_map, ("id",), ("name",), context=context)

    @put_many.register(Map)
    def put_many_map(self, items: Iterable[Map], context: PipelineContext = None) -> None:
        self._put_many(Map, items, uniquekeys.for_map, ("id",), ("name",), context=context)

    # Mastery

    @get.register(Mastery)
    @validate_query(uniquekeys.validate_mastery_query, uniquekeys.convert_region_to_platform)
    def get_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Mastery:
        return self._get(query, uniquekeys.for_mastery_query, context)

    @get_many.register(Mastery)
    @validate_query(uniquekeys.validate_many_mastery_query, uniquekeys.convert_region_to_platform)
    def get_many_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Mastery, None, None]:
        return self._get_many(query, uniquekeys.for_many_mastery_query, context)

    @put.register(Mastery)
    def put_mastery(self, item: Mastery, context: PipelineContext = None) -> None:
        self._put(Mastery, item, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    @put_many.register(Mastery)
    def put_many_mastery(self, items: Iterable[Mastery], context: PipelineContext = None) -> None:
        self._put_many(Mastery, items, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    # Profile Icon

    @get.register(ProfileIcon)
    @validate_query(uniquekeys.validate_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        return self._get(query, uniquekeys.for_profile_icon_query, context)

    @get_many.register(ProfileIcon)
    @validate_query(uniquekeys.validate_many_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_many_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIcon, None, None]:
        return self._get_many(query, uniquekeys.for_many_profile_icon_query, context)

    @put.register(ProfileIcon)
    def put_profile_icon(self, item: ProfileIcon, context: PipelineContext = None) -> None:
        self._put(ProfileIcon, item, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    @put_many.register(ProfileIcon)
    def put_many_profile_icon(self, items: Iterable[ProfileIcon], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcon, items, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    # Realm

    @get.register(Realms)
    @validate_query(uniquekeys.validate_realms_query, uniquekeys.convert_region_to_platform)
    def get_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Realms:
        return self._get(query, uniquekeys.for_realms_query, context)

    @get_many.register(Realms)
    @validate_query(uniquekeys.validate_many_realms_query, uniquekeys.convert_region_to_platform)
    def get_many_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Realms, None, None]:
        return self._get_many(query, uniquekeys.for_many_realms_query, context)

    @put.register(Realms)
    def put_realms(self, item: Realms, context: PipelineContext = None) -> None:
        self._put(Realms, item, uniquekeys.for_realms, context=context)

    @put_many.register(Realms)
    def put_many_realms(self, items: Iterable[Realms], context: PipelineContext = None) -> None:
        self._put_many(Realms, items, uniquekeys.for_realms, context=context)

    # Rune

    @get.register(Rune)
    @validate_query(uniquekeys.validate_rune_query, uniquekeys.convert_region_to_platform)
    def get_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Rune:
        return self._get(query, uniquekeys.for_rune_query, context)

    @get_many.register(Rune)
    @validate_query(uniquekeys.validate_many_rune_query, uniquekeys.convert_region_to_platform)
    def get_many_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Rune, None, None]:
        return self._get_many(query, uniquekeys.for_many_rune_query, context)

    @put.register(Rune)
    def put_rune(self, item: Rune, context: PipelineContext = None) -> None:
        self._put(Rune, item, uniquekeys.for_rune, ("id",), ("name",), context=context)

    @put_many.register(Rune)
    def put_many_rune(self, items: Iterable[Rune], context: PipelineContext = None) -> None:
        self._put_many(Rune, items, uniquekeys.for_rune, ("id",), ("name",), context=context)

    # Summoner Spell

    @get.register(SummonerSpell)
    @validate_query(uniquekeys.validate_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        return self._get(query, uniquekeys.for_summoner_spell_query, context)

    @get_many.register(SummonerSpell)
    @validate_query(uniquekeys.validate_many_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpell, None, None]:
        return self._get_many(query, uniquekeys.for_many_summoner_spell_query, context)

    @put.register(SummonerSpell)
    def put_summoner_spell(self, item: SummonerSpell, context: PipelineContext = None) -> None:
        self._put(SummonerSpell, item, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    @put_many.register(SummonerSpell)
    def put_many_summoner_spell(self, items: Iterable[SummonerSpell], context: PipelineContext = None) -> None:
        self._put_many(SummonerSpell, items, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    # Versions

    @get.register(Versions)
    @validate_query(uniquekeys.validate_versions_query, uniquekeys.convert_region_to_platform)
    def get_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Versions:
        return self._get(query, uniquekeys.for_versions_query, context)

    @get_many.register(Versions)
    @validate_query(uniquekeys.validate_many_versions_query, uniquekeys.convert_region_to_platform)
    def get_many_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Versions, None, None]:
        return self._get_many(query, uniquekeys.for_many_versions_query, context)

    @put.register(Versions)
    def put_versions(self, item: Versions, context: PipelineContext = None) -> None:
        self._put(Versions, item, uniquekeys.for_versions, context=context)

    @put_many.register(Versions)
    def put_many_versions(self, items: Iterable[Versions], context: PipelineContext = None) -> None:
        self._put_many(Versions, items, uniquekeys.for_versions, context=context)

    ##############
    # Status API #
    ##############

    @get.register(ShardStatus)
    @validate_query(uniquekeys.validate_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        return self._get(query, uniquekeys.for_shard_status_query, context)

    @get_many.register(ShardStatus)
    @validate_query(uniquekeys.validate_many_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_many_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ShardStatus, None, None]:
        return self._get_many(query, uniquekeys.for_many_shard_status_query, context)

    @put.register(ShardStatus)
    def put_shard_status(self, item: ShardStatus, context: PipelineContext = None) -> None:
        self._put(ShardStatus, item, uniquekeys.for_shard_status, context=context)

    @put_many.register(ShardStatus)
    def put_many_shard_status(self, items: Iterable[ShardStatus], context: PipelineContext = None) -> None:
        self._put_many(ShardStatus, items, uniquekeys.for_shard_status, context=context)

    #################
    # Masteries API #
    #################

    @get.register(MasteryPage)
    @validate_query(uniquekeys.validate_mastery_page_query, uniquekeys.convert_region_to_platform)
    def get_mastery_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasteryPage:
        return self._get(query, uniquekeys.for_mastery_page_query, context)

    @get_many.register(MasteryPage)
    @validate_query(uniquekeys.validate_many_mastery_page_query, uniquekeys.convert_region_to_platform)
    def get_many_mastery_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasteryPage, None, None]:
        return self._get_many(query, uniquekeys.for_many_mastery_page_query, context)

    @put.register(MasteryPage)
    def put_mastery_page(self, item: MasteryPage, context: PipelineContext = None) -> None:
        self._put(MasteryPage, item, uniquekeys.for_mastery_page, ("id",), ("account.id",), ("name",), context=context)

    @put_many.register(MasteryPage)
    def put_many_mastery_page(self, items: Iterable[MasteryPage], context: PipelineContext = None) -> None:
        self._put_many(MasteryPage, items, uniquekeys.for_mastery_page, ("id",), ("account.id",), ("name",), context=context)

    #############
    # Match API #
    #############

    @get.register(Match)
    @validate_query(uniquekeys.validate_match_query, uniquekeys.convert_region_to_platform)
    def get_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Match:
        return self._get(query, uniquekeys.for_match_query, context)

    @get_many.register(Match)
    @validate_query(uniquekeys.validate_many_match_query, uniquekeys.convert_region_to_platform)
    def get_many_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Match, None, None]:
        return self._get_many(query, uniquekeys.for_many_match_query, context)

    @put.register(Match)
    def put_match(self, item: Match, context: PipelineContext = None) -> None:
        self._put(Match, item, uniquekeys.for_match, context=context)

    @put_many.register(Match)
    def put_many_match(self, items: Iterable[Match], context: PipelineContext = None) -> None:
        self._put_many(Match, items, uniquekeys.for_match, context=context)

    #############
    # Runes API #
    #############

    @get.register(RunePage)
    @validate_query(uniquekeys.validate_rune_page_query, uniquekeys.convert_region_to_platform)
    def get_rune_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> RunePage:
        return self._get(query, uniquekeys.for_rune_page_query, context)

    @get_many.register(RunePage)
    @validate_query(uniquekeys.validate_many_rune_page_query, uniquekeys.convert_region_to_platform)
    def get_many_rune_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[RunePage, None, None]:
        return self._get_many(query, uniquekeys.for_many_rune_page_query, context)

    @put.register(RunePage)
    def put_rune_page(self, item: RunePage, context: PipelineContext = None) -> None:
        self._put(RunePage, item, uniquekeys.for_rune_page, ("id",), ("account.id",), ("name",), context=context)

    @put_many.register(RunePage)
    def put_many_rune_page(self, items: Iterable[RunePage], context: PipelineContext = None) -> None:
        self._put_many(RunePage, items, uniquekeys.for_rune_page, ("id",), ("account.id",), ("name",), context=context)

    #################
    # Spectator API #
    #################

    @get.register(CurrentMatch)
    @validate_query(uniquekeys.validate_current_match_query, uniquekeys.convert_region_to_platform)
    def get_current_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> CurrentMatch:
        return self._get(query, uniquekeys.for_current_match_query, context)

    @get_many.register(CurrentMatch)
    @validate_query(uniquekeys.validate_many_current_match_query, uniquekeys.convert_region_to_platform)
    def get_many_current_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[CurrentMatch, None, None]:
        return self._get_many(query, uniquekeys.for_many_current_match_query, context)

    @put.register(CurrentMatch)
    def put_current_match(self, item: CurrentMatch, context: PipelineContext = None) -> None:
        self._put(CurrentMatch, item, uniquekeys.for_current_match, context=context)

    @put_many.register(CurrentMatch)
    def put_many_current_match(self, items: Iterable[CurrentMatch], context: PipelineContext = None) -> None:
        self._put_many(CurrentMatch, items, uniquekeys.for_current_match, context=context)

    @get.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> FeaturedMatches:
        return self._get(query, uniquekeys.for_featured_matches_query, context)

    @get_many.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_many_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_many_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[FeaturedMatches, None, None]:
        return self._get_many(query, uniquekeys.for_many_featured_matches_query, context)

    @put.register(FeaturedMatches)
    def put_featured_matches(self, item: FeaturedMatches, context: PipelineContext = None) -> None:
        self._put(FeaturedMatches, item, uniquekeys.for_featured_matches, context=context)

    @put_many.register(FeaturedMatches)
    def put_many_featured_matches(self, items: Iterable[FeaturedMatches], context: PipelineContext = None) -> None:
        self._put_many(FeaturedMatches, items, uniquekeys.for_featured_matches, context=context)

    ################
    # Summoner API #
    ################

    @get.register(Summoner)
    @validate_query(uniquekeys.validate_summoner_query, uniquekeys.convert_region_to_platform)
    def get_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Summoner:
        return self._get(query, uniquekeys.for_summoner_query, context)

    @get_many.register(Summoner)
    @validate_query(uniquekeys.validate_many_summoner_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Summoner, None, None]:
        return self._get_many(query, uniquekeys.for_many_summoner_query, context)

    @put.register(Summoner)
    def put_summoner(self, item: Summoner, context: PipelineContext = None) -> None:
        self._put(Summoner, item, uniquekeys.for_summoner, ("id",), ("account.id",), ("name",), context=context)

    @put_many.register(Summoner)
    def put_many_summoner(self, items: Iterable[Summoner], context: PipelineContext = None) -> None:
        self._put_many(Summoner, items, uniquekeys.for_summoner, ("id",), ("account.id",), ("name",), context=context)
