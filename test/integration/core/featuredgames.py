from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/featuredgamesapi tests...")
    test_featured_games()


def test_featured_games():
    int_test_handler.test_result(riotapi.get_featured_games())
