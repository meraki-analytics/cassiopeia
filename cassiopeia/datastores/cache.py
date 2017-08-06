from typing import Type, Mapping, Any, Iterable, TypeVar, Tuple, Callable, Generator

from datapipelines import DataSource, DataSink, PipelineContext, validate_query, NotFoundError
from merakicommons.cache import Cache as CommonsCache

from . import uniquekeys
from ..core.championmastery import ChampionMastery
from ..core.league import Leagues, ChallengerLeague, MasterLeague
from ..core.staticdata import Champion, Mastery, Rune, Item, SummonerSpell, Map, Realms, ProfileIcon, Locales, LanguageStrings, Versions, SummonerSpells, Items, Champions, Masteries, Runes, Maps, ProfileIcons
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

    def _get(self, type: Any, query: Mapping[str, Any], key_function: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None):
        key = key_function(query)
        try:
            return self._cache.get(type, key)
        except KeyError as e:
            raise NotFoundError from e

    def _get_many(self, type: Any, query: Mapping[str, Any], key_generator: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None):
        for key in key_generator(query):
            try:
                yield self._cache.get(type, key)
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
            self._cache.put(type, key, item, expire_seconds)
        else:
            for key_function_args in key_function_arg_lists:
                key = key_function(item, *key_function_args)
                self._cache.put(type, key, item, expire_seconds)
        # TODO: Put EXPIRATION into context once cache expiration works

    def _put_many(self, type: Type[T], items: Iterable[T], key_function: Callable[[T], Any], *key_function_arg_lists: tuple, context: PipelineContext = None) -> None:
        try:
            expire_seconds = self._expiration[type]
        except KeyError:
            expire_seconds = -1.0

        for key, item in Cache._put_many_generator(items, key_function, *key_function_arg_lists):
            self._cache.put(type, key, item, expire_seconds)
        # TODO: Put EXPIRATION into context once cache expiration works

    ########################
    # Champion Mastery API #
    ########################

    @get.register(ChampionMastery)
    @validate_query(uniquekeys.validate_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champion:
        return self._get(ChampionMastery, query, uniquekeys.for_champion_mastery_query, context)

    @get_many.register(ChampionMastery)
    @validate_query(uniquekeys.validate_many_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_many_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champion, None, None]:
        return self._get_many(ChampionMastery, query, uniquekeys.for_many_champion_mastery_query, context)

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

    @get.register(Leagues)
    @validate_query(uniquekeys.validate_leagues_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Leagues:
        return self._get(Leagues, query, uniquekeys.for_leagues_query, context)

    @get_many.register(Leagues)
    @validate_query(uniquekeys.validate_many_leagues_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Leagues, None, None]:
        return self._get_many(Leagues, query, uniquekeys.for_many_leagues_query, context)

    @put.register(Leagues)
    def put_league_summoner(self, item: Leagues, context: PipelineContext = None) -> None:
        self._put(Leagues, item, uniquekeys.for_leagues, context=context)

    @put_many.register(Leagues)
    def put_many_league_summoner(self, items: Iterable[Leagues], context: PipelineContext = None) -> None:
        self._put_many(Leagues, items, uniquekeys.for_leagues, context=context)

    # Challenger

    @get.register(ChallengerLeague)
    @validate_query(uniquekeys.validate_challenger_league_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChallengerLeague:
        return self._get(ChallengerLeague, query, uniquekeys.for_challenger_league_query, context)

    @get_many.register(ChallengerLeague)
    @validate_query(uniquekeys.validate_many_challenger_league_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChallengerLeague, None, None]:
        return self._get_many(ChallengerLeague, query, uniquekeys.for_many_challenger_league_query, context)

    @put.register(ChallengerLeague)
    def put_league_summoner(self, item: ChallengerLeague, context: PipelineContext = None) -> None:
        self._put(ChallengerLeague, item, uniquekeys.for_challenger_league, context=context)

    @put_many.register(ChallengerLeague)
    def put_many_league_summoner(self, items: Iterable[ChallengerLeague], context: PipelineContext = None) -> None:
        self._put_many(ChallengerLeague, items, uniquekeys.for_challenger_league, context=context)

    # Master

    @get.register(MasterLeague)
    @validate_query(uniquekeys.validate_master_league_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        return self._get(MasterLeague, query, uniquekeys.for_master_league_query, context)

    @get_many.register(MasterLeague)
    @validate_query(uniquekeys.validate_many_master_league_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasterLeague, None, None]:
        return self._get_many(MasterLeague, query, uniquekeys.for_many_master_league_query, context)

    @put.register(MasterLeague)
    def put_league_summoner(self, item: MasterLeague, context: PipelineContext = None) -> None:
        self._put(MasterLeague, item, uniquekeys.for_master_league, context=context)

    @put_many.register(MasterLeague)
    def put_many_league_summoner(self, items: Iterable[MasterLeague], context: PipelineContext = None) -> None:
        self._put_many(MasterLeague, items, uniquekeys.for_master_league, context=context)

    ###################
    # Static Data API #
    ###################
    
    # Champion

    @get.register(Champion)
    @validate_query(uniquekeys.validate_champion_query, uniquekeys.convert_region_to_platform)
    def get_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champion:
        return self._get(Champion, query, uniquekeys.for_champion_query, context)

    @get_many.register(Champion)
    @validate_query(uniquekeys.validate_many_champion_query, uniquekeys.convert_region_to_platform)
    def get_many_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champion, None, None]:
        return self._get_many(Champion, query, uniquekeys.for_many_champion_query, context)

    @put.register(Champion)
    def put_champion(self, item: Champion, context: PipelineContext = None) -> None:
        self._put(Champion, item, uniquekeys.for_champion, ("id",), ("name",), context=context)

    @put_many.register(Champion)
    def put_many_champion(self, items: Iterable[Champion], context: PipelineContext = None) -> None:
        self._put_many(Champion, items, uniquekeys.for_champion, ("id",), ("name",), context=context)

    @get.register(Champions)
    @validate_query(uniquekeys.validate_champions_query, uniquekeys.convert_region_to_platform)
    def get_champions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champions:
        return self._get(Champions, query, uniquekeys.for_champions_query, context)

    @get_many.register(Champions)
    @validate_query(uniquekeys.validate_many_champions_query, uniquekeys.convert_region_to_platform)
    def get_many_champions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champions, None, None]:
        return self._get_many(Champions, query, uniquekeys.for_many_champions_query, context)

    @put.register(Champions)
    def put_champions(self, champions: Champions, context: PipelineContext = None) -> None:
        self._put(Champions, champions, uniquekeys.for_champions, ("platform",), context=context)
        for champion in champions:
            self._put(Champion, champion, uniquekeys.for_champion, ("id",), ("name",), context=context)

    @put_many.register(Champions)
    def put_many_champions(self, champions: Iterable[Champions], context: PipelineContext = None) -> None:
        self._put_many(Champions, champions, uniquekeys.for_champions, ("platform",), context=context)
        for champion in champions:
            self._put(Champion, champion, uniquekeys.for_champion, ("id",), ("name",), context=context)

    # Item

    @get.register(Item)
    @validate_query(uniquekeys.validate_item_query, uniquekeys.convert_region_to_platform)
    def get_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Item:
        return self._get(Item, query, uniquekeys.for_item_query, context)

    @get_many.register(Item)
    @validate_query(uniquekeys.validate_many_item_query, uniquekeys.convert_region_to_platform)
    def get_many_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Item, None, None]:
        return self._get_many(Item, query, uniquekeys.for_many_item_query, context)

    @put.register(Item)
    def put_item(self, item: Item, context: PipelineContext = None) -> None:
        self._put(Item, item, uniquekeys.for_item, ("id",), ("name",), context=context)

    @put_many.register(Item)
    def put_many_item(self, items: Iterable[Item], context: PipelineContext = None) -> None:
        self._put_many(Item, items, uniquekeys.for_item, ("id",), ("name",), context=context)

    @get.register(Items)
    @validate_query(uniquekeys.validate_items_query, uniquekeys.convert_region_to_platform)
    def get_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Items:
        return self._get(Items, query, uniquekeys.for_items_query, context)

    @get_many.register(Items)
    @validate_query(uniquekeys.validate_many_items_query, uniquekeys.convert_region_to_platform)
    def get_many_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Items, None, None]:
        return self._get_many(Items, query, uniquekeys.for_many_items_query, context)

    @put.register(Items)
    def put_items(self, items: Items, context: PipelineContext = None) -> None:
        self._put(Items, items, uniquekeys.for_items, ("platform",), context=context)
        for item in items:
            self._put(Item, item, uniquekeys.for_item, ("id",), ("name",), context=context)

    @put_many.register(Items)
    def put_many_items(self, items: Iterable[Items], context: PipelineContext = None) -> None:
        self._put_many(Items, items, uniquekeys.for_items, ("platform",), context=context)
        for item in items:
            self._put(Item, item, uniquekeys.for_item, ("id",), ("name",), context=context)

    # Language

    @get.register(Locales)
    @validate_query(uniquekeys.validate_languages_query, uniquekeys.convert_region_to_platform)
    def get_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Locales:
        return self._get(Locales, query, uniquekeys.for_languages_query, context)

    @get_many.register(Locales)
    @validate_query(uniquekeys.validate_many_languages_query, uniquekeys.convert_region_to_platform)
    def get_many_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Locales, None, None]:
        return self._get_many(Locales, query, uniquekeys.for_many_languages_query, context)

    @put.register(Locales)
    def put_languages(self, item: Locales, context: PipelineContext = None) -> None:
        self._put(Locales, item, uniquekeys.for_languages, context=context)

    @put_many.register(Locales)
    def put_many_languages(self, items: Iterable[Locales], context: PipelineContext = None) -> None:
        self._put_many(Locales, items, uniquekeys.for_languages, context=context)

    @get.register(LanguageStrings)
    @validate_query(uniquekeys.validate_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        return self._get(LanguageStrings, query, uniquekeys.for_language_strings_query, context)

    @get_many.register(LanguageStrings)
    @validate_query(uniquekeys.validate_many_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_many_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LanguageStrings, None, None]:
        return self._get_many(LanguageStrings, query, uniquekeys.for_many_language_strings_query, context)

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
        return self._get(Map, query, uniquekeys.for_map_query, context)

    @get_many.register(Map)
    @validate_query(uniquekeys.validate_many_map_query, uniquekeys.convert_region_to_platform)
    def get_many_map(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Map, None, None]:
        return self._get_many(Map, query, uniquekeys.for_many_map_query, context)

    @put.register(Map)
    def put_map(self, item: Map, context: PipelineContext = None) -> None:
        self._put(Map, item, uniquekeys.for_map, ("id",), ("name",), context=context)

    @put_many.register(Map)
    def put_many_map(self, items: Iterable[Map], context: PipelineContext = None) -> None:
        self._put_many(Map, items, uniquekeys.for_map, ("id",), ("name",), context=context)

    @get.register(Maps)
    @validate_query(uniquekeys.validate_maps_query, uniquekeys.convert_region_to_platform)
    def get_maps(self, query: Mapping[str, Any], context: PipelineContext = None) -> Maps:
        return self._get(Maps, query, uniquekeys.for_maps_query, context)

    @get_many.register(Maps)
    @validate_query(uniquekeys.validate_many_maps_query, uniquekeys.convert_region_to_platform)
    def get_many_maps(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Maps, None, None]:
        return self._get_many(Maps, query, uniquekeys.for_many_maps_query, context)

    @put.register(Maps)
    def put_maps(self, item: Maps, context: PipelineContext = None) -> None:
        self._put(Maps, item, uniquekeys.for_maps, ("id",), ("name",), context=context)
        for map in item:
            self._put(Map, map, uniquekeys.for_map, ("id",), ("name",), context=context)

    @put_many.register(Maps)
    def put_many_maps(self, items: Iterable[Maps], context: PipelineContext = None) -> None:
        self._put_many(Maps, items, uniquekeys.for_maps, ("id",), ("name",), context=context)
        for maps in items:
            self._put_many(Map, maps, uniquekeys.for_map, ("id",), ("name",), context=context)

    # Mastery

    @get.register(Mastery)
    @validate_query(uniquekeys.validate_mastery_query, uniquekeys.convert_region_to_platform)
    def get_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Mastery:
        return self._get(Mastery, query, uniquekeys.for_mastery_query, context)

    @get_many.register(Mastery)
    @validate_query(uniquekeys.validate_many_mastery_query, uniquekeys.convert_region_to_platform)
    def get_many_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Mastery, None, None]:
        return self._get_many(Mastery, query, uniquekeys.for_many_mastery_query, context)

    @put.register(Mastery)
    def put_mastery(self, item: Mastery, context: PipelineContext = None) -> None:
        self._put(Mastery, item, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    @put_many.register(Mastery)
    def put_many_mastery(self, items: Iterable[Mastery], context: PipelineContext = None) -> None:
        self._put_many(Mastery, items, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    @get.register(Masteries)
    @validate_query(uniquekeys.validate_masteries_query, uniquekeys.convert_region_to_platform)
    def get_masteries(self, query: Mapping[str, Any], context: PipelineContext = None) -> Masteries:
        return self._get(Masteries, query, uniquekeys.for_masteries_query, context)

    @get_many.register(Masteries)
    @validate_query(uniquekeys.validate_many_masteries_query, uniquekeys.convert_region_to_platform)
    def get_many_masteries(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Masteries, None, None]:
        return self._get_many(Masteries, query, uniquekeys.for_many_masteries_query, context)

    @put.register(Masteries)
    def put_masteries(self, item: Masteries, context: PipelineContext = None) -> None:
        self._put(Masteries, item, uniquekeys.for_masteries, ("id",), ("name",), context=context)
        for mastery in item:
            self._put(Mastery, mastery, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    @put_many.register(Masteries)
    def put_many_masteries(self, items: Iterable[Masteries], context: PipelineContext = None) -> None:
        self._put_many(Masteries, items, uniquekeys.for_masteries, ("id",), ("name",), context=context)
        for mastery in items:
            self._put(Mastery, mastery, uniquekeys.for_mastery, ("id",), ("name",), context=context)

    # Profile Icon

    @get.register(ProfileIcon)
    @validate_query(uniquekeys.validate_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        return self._get(ProfileIcon, query, uniquekeys.for_profile_icon_query, context)

    @get_many.register(ProfileIcon)
    @validate_query(uniquekeys.validate_many_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_many_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIcon, None, None]:
        return self._get_many(ProfileIcon, query, uniquekeys.for_many_profile_icon_query, context)

    @put.register(ProfileIcon)
    def put_profile_icon(self, item: ProfileIcon, context: PipelineContext = None) -> None:
        self._put(ProfileIcon, item, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    @put_many.register(ProfileIcon)
    def put_many_profile_icon(self, items: Iterable[ProfileIcon], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcon, items, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    @get.register(ProfileIcons)
    @validate_query(uniquekeys.validate_profile_icons_query, uniquekeys.convert_region_to_platform)
    def get_profile_icons(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        return self._get(ProfileIcons, query, uniquekeys.for_profile_icons_query, context)

    @get_many.register(ProfileIcons)
    @validate_query(uniquekeys.validate_many_profile_icons_query, uniquekeys.convert_region_to_platform)
    def get_many_profile_icons(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIcons, None, None]:
        return self._get_many(ProfileIcons, query, uniquekeys.for_many_profile_icons_query, context)

    @put.register(ProfileIcons)
    def put_profile_icons(self, item: ProfileIcons, context: PipelineContext = None) -> None:
        self._put(ProfileIcons, item, uniquekeys.for_profile_icons, ("id",), ("name",), context=context)
        for profile_icon in item:
            self._put(ProfileIcon, profile_icon, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    @put_many.register(ProfileIcons)
    def put_many_profile_icons(self, items: Iterable[ProfileIcons], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcons, items, uniquekeys.for_profile_icons, ("id",), ("name",), context=context)
        for profile_icon in items:
            self._put(ProfileIcon, profile_icon, uniquekeys.for_profile_icon, ("id",), ("name",), context=context)

    # Realm

    @get.register(Realms)
    @validate_query(uniquekeys.validate_realms_query, uniquekeys.convert_region_to_platform)
    def get_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Realms:
        return self._get(Realms, query, uniquekeys.for_realms_query, context)

    @get_many.register(Realms)
    @validate_query(uniquekeys.validate_many_realms_query, uniquekeys.convert_region_to_platform)
    def get_many_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Realms, None, None]:
        return self._get_many(Realms, query, uniquekeys.for_many_realms_query, context)

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
        return self._get(Rune, query, uniquekeys.for_rune_query, context)

    @get_many.register(Rune)
    @validate_query(uniquekeys.validate_many_rune_query, uniquekeys.convert_region_to_platform)
    def get_many_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Rune, None, None]:
        return self._get_many(Rune, query, uniquekeys.for_many_rune_query, context)

    @put.register(Rune)
    def put_rune(self, item: Rune, context: PipelineContext = None) -> None:
        self._put(Rune, item, uniquekeys.for_rune, ("id",), ("name",), context=context)

    @put_many.register(Rune)
    def put_many_rune(self, items: Iterable[Rune], context: PipelineContext = None) -> None:
        self._put_many(Rune, items, uniquekeys.for_rune, ("id",), ("name",), context=context)

    @get.register(Runes)
    @validate_query(uniquekeys.validate_runes_query, uniquekeys.convert_region_to_platform)
    def get_runes(self, query: Mapping[str, Any], context: PipelineContext = None) -> Runes:
        return self._get(Runes, query, uniquekeys.for_runes_query, context)

    @get_many.register(Runes)
    @validate_query(uniquekeys.validate_many_runes_query, uniquekeys.convert_region_to_platform)
    def get_many_runes(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Runes, None, None]:
        return self._get_many(Runes, query, uniquekeys.for_many_runes_query, context)

    @put.register(Runes)
    def put_runes(self, item: Runes, context: PipelineContext = None) -> None:
        self._put(Runes, item, uniquekeys.for_runes, ("id",), ("name",), context=context)
        for rune in item:
            self._put(Mastery, rune, uniquekeys.for_rune, ("id",), ("name",), context=context)

    @put_many.register(Runes)
    def put_many_runes(self, items: Iterable[Runes], context: PipelineContext = None) -> None:
        self._put_many(Runes, items, uniquekeys.for_runes, ("id",), ("name",), context=context)
        for rune in items:
            self._put(Mastery, rune, uniquekeys.for_rune, ("id",), ("name",), context=context)

    # Summoner Spell

    @get.register(SummonerSpell)
    @validate_query(uniquekeys.validate_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        return self._get(SummonerSpell, query, uniquekeys.for_summoner_spell_query, context)

    @get_many.register(SummonerSpell)
    @validate_query(uniquekeys.validate_many_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpell, None, None]:
        return self._get_many(SummonerSpell, query, uniquekeys.for_many_summoner_spell_query, context)

    @put.register(SummonerSpell)
    def put_summoner_spell(self, item: SummonerSpell, context: PipelineContext = None) -> None:
        self._put(SummonerSpell, item, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    @put_many.register(SummonerSpell)
    def put_many_summoner_spell(self, items: Iterable[SummonerSpell], context: PipelineContext = None) -> None:
        self._put_many(SummonerSpell, items, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    @get.register(SummonerSpells)
    @validate_query(uniquekeys.validate_summoner_spells_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spells(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpells:
        return self._get(SummonerSpells, query, uniquekeys.for_summoner_spells_query, context)

    @get_many.register(SummonerSpells)
    @validate_query(uniquekeys.validate_many_summoner_spells_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner_spells(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpells, None, None]:
        return self._get_many(SummonerSpells, query, uniquekeys.for_many_summoner_spells_query, context)

    @put.register(SummonerSpells)
    def put_summoner_spells(self, item: SummonerSpells, context: PipelineContext = None) -> None:
        self._put(SummonerSpells, item, uniquekeys.for_summoner_spells, ("id",), ("name",), context=context)
        for summoner_spell in item:
            self._put(Mastery, summoner_spell, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    @put_many.register(SummonerSpells)
    def put_many_summoner_spells(self, items: Iterable[SummonerSpells], context: PipelineContext = None) -> None:
        self._put_many(SummonerSpells, items, uniquekeys.for_summoner_spells, ("id",), ("name",), context=context)
        for summoner_spell in items:
            self._put(Mastery, summoner_spell, uniquekeys.for_summoner_spell, ("id",), ("name",), context=context)

    # Versions

    @get.register(Versions)
    @validate_query(uniquekeys.validate_versions_query, uniquekeys.convert_region_to_platform)
    def get_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Versions:
        return self._get(Versions, query, uniquekeys.for_versions_query, context=context)

    @get_many.register(Versions)
    @validate_query(uniquekeys.validate_many_versions_query, uniquekeys.convert_region_to_platform)
    def get_many_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Versions, None, None]:
        return self._get_many(Versions, query, uniquekeys.for_many_versions_query, context=context)

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
        return self._get(ShardStatus, query, uniquekeys.for_shard_status_query, context)

    @get_many.register(ShardStatus)
    @validate_query(uniquekeys.validate_many_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_many_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ShardStatus, None, None]:
        return self._get_many(ShardStatus, query, uniquekeys.for_many_shard_status_query, context)

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
        return self._get(MasteryPage, query, uniquekeys.for_mastery_page_query, context)

    @get_many.register(MasteryPage)
    @validate_query(uniquekeys.validate_many_mastery_page_query, uniquekeys.convert_region_to_platform)
    def get_many_mastery_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasteryPage, None, None]:
        return self._get_many(MasteryPage, query, uniquekeys.for_many_mastery_page_query, context)

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
        return self._get(Match, query, uniquekeys.for_match_query, context)

    @get_many.register(Match)
    @validate_query(uniquekeys.validate_many_match_query, uniquekeys.convert_region_to_platform)
    def get_many_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Match, None, None]:
        return self._get_many(Match, query, uniquekeys.for_many_match_query, context)

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
        return self._get(RunePage, query, uniquekeys.for_rune_page_query, context)

    @get_many.register(RunePage)
    @validate_query(uniquekeys.validate_many_rune_page_query, uniquekeys.convert_region_to_platform)
    def get_many_rune_page(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[RunePage, None, None]:
        return self._get_many(RunePage, query, uniquekeys.for_many_rune_page_query, context)

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
        return self._get(CurrentMatch, query, uniquekeys.for_current_match_query, context)

    @get_many.register(CurrentMatch)
    @validate_query(uniquekeys.validate_many_current_match_query, uniquekeys.convert_region_to_platform)
    def get_many_current_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[CurrentMatch, None, None]:
        return self._get_many(CurrentMatch, query, uniquekeys.for_many_current_match_query, context)

    @put.register(CurrentMatch)
    def put_current_match(self, item: CurrentMatch, context: PipelineContext = None) -> None:
        self._put(CurrentMatch, item, uniquekeys.for_current_match, context=context)

    @put_many.register(CurrentMatch)
    def put_many_current_match(self, items: Iterable[CurrentMatch], context: PipelineContext = None) -> None:
        self._put_many(CurrentMatch, items, uniquekeys.for_current_match, context=context)

    @get.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> FeaturedMatches:
        return self._get(FeaturedMatches, query, uniquekeys.for_featured_matches_query, context)

    @get_many.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_many_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_many_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[FeaturedMatches, None, None]:
        return self._get_many(FeaturedMatches, query, uniquekeys.for_many_featured_matches_query, context)

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
        return self._get(Summoner, query, uniquekeys.for_summoner_query, context)

    @get_many.register(Summoner)
    @validate_query(uniquekeys.validate_many_summoner_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Summoner, None, None]:
        return self._get_many(Summoner, query, uniquekeys.for_many_summoner_query, context)

    @put.register(Summoner)
    def put_summoner(self, item: Summoner, context: PipelineContext = None) -> None:
        self._put(Summoner, item, uniquekeys.for_summoner, ("id",), ("account.id",), ("name",), context=context)

    @put_many.register(Summoner)
    def put_many_summoner(self, items: Iterable[Summoner], context: PipelineContext = None) -> None:
        self._put_many(Summoner, items, uniquekeys.for_summoner, ("id",), ("account.id",), ("name",), context=context)
