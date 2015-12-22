import dto.all
import core.all
import int_test_handler

def test_all():
    dto.all.test_all()
    core.all.test_all()


def test_all_integrations():
    assert test_all()
