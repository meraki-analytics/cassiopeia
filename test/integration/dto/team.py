from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/team tests...")
    test_teams_by_summoner_id()
    test_teams_by_id()


def test_teams_by_summoner_id():
    int_test_handler.test_result(baseriotapi.get_teams_by_summoner_id(int_test_handler.summoner_id))


def test_teams_by_id():
    int_test_handler.test_result(baseriotapi.get_teams_by_id(int_test_handler.team_id))
