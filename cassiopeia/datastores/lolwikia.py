import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, validate_query

from ..data import Platform
from ..dto.staticdata.champion import ChampionReleaseDto, ChampionReleasesDto, ChampionListDto
from .common import HTTPClient
from .uniquekeys import convert_region_to_platform

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class LolWikia(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._cache = {}

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_release_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str)

    @get.register(ChampionReleaseDto)
    @validate_query(_validate_get_champion_release_query, convert_region_to_platform)
    def get_champion_release(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionReleaseDto:
        releases_query = copy.deepcopy(query)
        releases_query.pop("id", None)
        releases_query.pop("name", None)
        releases = context[context.Keys.PIPELINE].get(ChampionReleasesDto, query=releases_query)

        if "name" not in query:
            champions = context[context.Keys.PIPELINE].get(ChampionListDto, query=releases_query)
            champion_name = [champion for champion in champions if champion["id"] == query["id"]][0]["name"]
        else:
            champion_name = query["name"]
        return ChampionReleaseDto({"releaseDate": releases[champion_name]})

    _validate_get_champion_releases_query = Query. \
        has("platform").as_(Platform)

    @get.register(ChampionReleasesDto)
    @validate_query(_validate_get_champion_releases_query, convert_region_to_platform)
    def get_champion_releases(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionReleasesDto:
        try:
            return self._cache[ChampionReleasesDto]
        except KeyError:
            import requests
            from bs4 import BeautifulSoup
            import arrow

            page = requests.get("http://leagueoflegends.wikia.com/wiki/List_of_champions")
            soup = BeautifulSoup(page.text, "html.parser")
            table = soup.find_all("table", {"class": "wikitable"})[1]

            rows = table.find_all('tr')[1:]
            for i, row in enumerate(rows):
                row = [r.text.strip() for r in row.find_all('td')]
                row = [str(row[0]), row[3]]
                try:
                    row[0] = row[0][:row[0].index("\xa0")]
                except ValueError:
                    pass
                try:
                    row[0] = row[0][:row[0].index(",")]
                except ValueError:
                    pass
                row[1] = arrow.get(row[1])
                rows[i] = row

            releases = {row[0]: row[1] for row in rows if row[1] < arrow.now()}

            # Manually fix names that are inconsistent
            if "Nunu & Willump" not in releases and "Nunu" in releases:
                releases["Nunu & Willump"] = releases.pop("Nunu")

            releases = ChampionReleasesDto(releases)
            self._cache[ChampionReleasesDto] = releases
            return releases
