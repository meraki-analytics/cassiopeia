from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/currentgameapi tests...")
    test_current_game()


def test_current_game():
    int_test_handler.test_result(baseriotapi.get_current_game(int_test_handler.summoner_id))
