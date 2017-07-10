import pytest

from cassiopeia.patches import patches, Patch


def test_known_patches():
    assert isinstance(Patch.from_str('0.9.22.4'), Patch)
    assert isinstance(Patch.from_str('5.19'), Patch)


def test_unknown_patch_raises():
    with pytest.raises(ValueError):
        Patch.from_str("unknown patch")


def test_patches_sorted():
    assert sorted(patches, key=lambda p: p.start) == patches


def test_major():
    assert patches[0].major == '0'
    assert Patch.from_str('6.10').major == '6'


def test_minor():
    assert patches[0].minor == '9'
    assert Patch.from_str('6.10').minor == '10'


def test_majorminor():
    assert patches[0].majorminor == '0.9'
    assert Patch.from_str('6.10').majorminor == '6.10'


def test_revision():
    assert patches[0].revision == '22.4'
    assert Patch.from_str('6.10').revision == ''

