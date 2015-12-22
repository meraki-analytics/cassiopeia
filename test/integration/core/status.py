from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/status tests...")
    test_shards()
    test_shard()


def test_shards():
    int_test_handler.test_result(riotapi.get_shards())


def test_shard():
    int_test_handler.test_result(riotapi.get_shard())
