from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/gameapi tests...")
    test_recent_games()


def test_recent_games():
    int_test_handler.test_result(riotapi.get_recent_games(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))
