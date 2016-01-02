from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/gameapi tests...")
    test_recent_games()


def test_recent_games():
    int_test_handler.test_result(baseriotapi.get_recent_games(int_test_handler.summoner_id))
