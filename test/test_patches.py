import pytest

from cassiopeia import Patch, Season, Region


def test_known_patches():
    assert isinstance(Patch.from_str('1.0.0.152', region="NA"), Patch)
    assert isinstance(Patch.from_str('5.19', region="NA"), Patch)
    assert isinstance(Patch.from_str('7.22', region="NA"), Patch)


def test_unknown_patch_raises():
    with pytest.raises(ValueError):
        Patch.from_str("unknown patch")

def test_season_start_end_using_patches():
    assert Season.season_7.start(Region.north_america) == Patch.from_str("7.1", region=Region.north_america).start
    assert Season.season_8.end(Region.north_america) == None


def test_patch_relational_operators():
    assert Patch.from_str("9.9", region="NA") < Patch.from_str("9.10", region="NA")
    assert Patch.from_str("8.20", region="NA") > Patch.from_str("8.11", region="NA")
    assert Patch.from_str("8.20", region="NA") > Patch.from_str("8.3", region="NA")
