import pytest

from cassiopeia import Patch


def test_known_patches():
    assert isinstance(Patch.from_str('0.9.22.4', region="NA"), Patch)
    assert isinstance(Patch.from_str('5.19', region="NA"), Patch)
    assert isinstance(Patch.from_str('7.22', region="NA"), Patch)


def test_unknown_patch_raises():
    with pytest.raises(ValueError):
        Patch.from_str("unknown patch")

