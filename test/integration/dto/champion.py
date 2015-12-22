from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/championapi tests...")
    test_champion_status()
    test_champion_statuses()


def test_champion_status():
    int_test_handler.test_result(baseriotapi.get_champion_status(int_test_handler.champion_id))


def test_champion_statuses():
    int_test_handler.test_result(baseriotapi.get_champion_statuses())
