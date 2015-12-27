from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/currentgameapi tests...")
    test_current_game()


def test_current_game():
    int_test_handler.test_result(riotapi.get_current_game(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))
