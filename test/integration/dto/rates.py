from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/requests tests...")
    test_tracking_on_valid_request()


def test_tracking_on_valid_request():
    """Checks that the request tracking works on requests with expected return code of 200"""
    int_test_handler.test_result(baseriotapi.get_requests_count() == (0,0))
    int_test_handler.test_result(baseriotapi.get_match(int_test_handler.match_id))
    int_test_handler.test_result(baseriotapi.get_requests_count() == (1,1))

def test_tracking_on_404_request():
    """Checks that the request tracking works on requests which raise exceptions"""
    int_test_handler.test_result(baseriotapi.get_requests_count() == (0,0))
    int_test_handler.test_result(baseriotapi.get_champion(int_test_handler.non_existent_champion_id))
    int_test_handler.test_result(baseriotapi.get_requests_count() == (0,1))