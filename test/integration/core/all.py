import champion
import currentgame
import featuredgames
import game
import league
import match
import matchlist
import staticdata
import stats
import status
import summoner
import team
from cassiopeia import riotapi


def test_all():
    print("core tests...")
    riotapi.get_items()
    riotapi.get_champions()
    riotapi.get_runes()
    riotapi.get_masteries()
    riotapi.get_summoner_spells()

    champion.test_all()
    currentgame.test_all()
    featuredgames.test_all()
    game.test_all()
    league.test_all()
    match.test_all()
    matchlist.test_all()
    staticdata.test_all()
    stats.test_all()
    status.test_all()
    summoner.test_all()
    team.test_all()
