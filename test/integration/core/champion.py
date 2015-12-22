from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/championapi tests...")
    test_champion_status()
    test_champion_statuses()


def test_champion_status():
    int_test_handler.test_result(riotapi.get_champion_status(riotapi.get_champion_by_id(int_test_handler.champion_id)))


def test_champion_statuses():
    int_test_handler.test_result(riotapi.get_champion_statuses())
