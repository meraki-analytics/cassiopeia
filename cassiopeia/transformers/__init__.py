from datapipelines import CompositeDataTransformer

from .staticdata import StaticDataTransformer
from .champion import ChampionTransformer
from .championmastery import ChampionMasteryTransformer
from .summoner import SummonerTransformer
from .match import MatchTransformer
from .spectator import SpectatorTransformer
from .status import StatusTransformer
from .leagues import LeagueTransformer
from .thirdpartycode import ThirdPartyCodeTransformer


riotapi_transformer = CompositeDataTransformer([
    StaticDataTransformer(),
    ChampionTransformer(),
    ChampionMasteryTransformer(),
    SummonerTransformer(),
    MatchTransformer(),
    SpectatorTransformer(),
    StatusTransformer(),
    LeagueTransformer(),
    ThirdPartyCodeTransformer()
])

__transformers__ = [riotapi_transformer]
