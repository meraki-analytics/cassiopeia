import os

from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


RIOT_API_KEY = os.environ.get("RIOT_API_KEY")

if RIOT_API_KEY:
    riotapi.set_api_key(os.environ["RIOT_API_KEY"])
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    riotapi.set_load_policy(LoadPolicy.lazy)

non_existent_champion_id = 1000
champion_id = 35
champion_name = "Thresh"
mastery_id = 6361
match_id = 1505030444
rune_id = 5234
summoner_id = 22508641
summoner_name = "FatalElement"
summoner_spell_id = 7
team_id = "TEAM-49fc9f10-1290-11e3-80a6-782bcb4d0bb2"
item_id = 3031


def test_result(result=None):
    assert True  # ??? was Pass previously
