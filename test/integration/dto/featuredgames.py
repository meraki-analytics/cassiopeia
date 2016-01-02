from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/featuredgamesapi tests...")
    test_featured_games()


def test_featured_games():
    int_test_handler.test_result(baseriotapi.get_featured_games())
