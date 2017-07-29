import cassiopeia
import pytest

from merakicommons.container import SearchableList, SearchError

from .constants import CHAMP_NAME


def test_returns_correct_type():
    champ = cassiopeia.get_champion(CHAMP_NAME)
    all_champs = cassiopeia.get_champions()

    assert isinstance(champ, cassiopeia.Champion)
    assert isinstance(all_champs, SearchableList)
    assert all(isinstance(c, cassiopeia.Champion) for c in all_champs)


def test_raises_with_unknown_champion():
    with pytest.raises(SearchError):
        cassiopeia.get_champion('nonexistant champ')


def test_champion_and_champions_return_same_data():
    champions = cassiopeia.get_champions()

    champ = champions[0]
    from_get_champion = cassiopeia.get_champion(champ.name)

    assert champ.__dict__ == from_get_champion.__dict__
