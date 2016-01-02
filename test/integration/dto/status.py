from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/status tests...")
    test_shards()
    test_shard()


def test_shards():
    int_test_handler.test_result(baseriotapi.get_shards())


def test_shard():
    int_test_handler.test_result(baseriotapi.get_shard())
