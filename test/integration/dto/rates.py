from cassiopeia import baseriotapi
from .. import int_test_handler


def test_tracking_on_valid_request():
    """Checks that the request tracking works on requests with expected return code of 200"""
    start_count = baseriotapi.get_requests_count()
    int_test_handler.test_result(baseriotapi.get_match(int_test_handler.match_id))
    int_test_handler.test_result(baseriotapi.get_requests_count() == (start_count[0] + 1, start_count[1] + 1))


def test_tracking_on_404_request():
    """Checks that the request tracking works on requests which raise exceptions"""
    start_count = baseriotapi.get_requests_count()
    try:
        baseriotapi.get_champion(int_test_handler.non_existent_champion_id)
    except:
        pass
    int_test_handler.test_result(baseriotapi.get_requests_count() == (start_count[0], start_count[1] + 1))
