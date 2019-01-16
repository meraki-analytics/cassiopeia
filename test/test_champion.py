import cassiopeia
import pytest

from merakicommons.container import SearchableList, SearchError

from .constants import CHAMP_NAME


def test_returns_correct_type():
    champion = cassiopeia.get_champion(CHAMP_NAME, region="NA")
    champions = cassiopeia.get_champions(region="NA")

    assert isinstance(champion, cassiopeia.Champion)
    assert isinstance(champions, SearchableList)
    assert all(isinstance(c, cassiopeia.Champion) for c in champions)


def test_raises_with_unknown_champion():
    with pytest.raises(SearchError):
        cassiopeia.get_champion('nonexistant champ', region="NA")


def test_champion_and_champions_return_same_data():
    champions = cassiopeia.get_champions(region="NA")

    champion = champions[0]
    from_get_champion = cassiopeia.get_champion(champion.name, region="NA")

    assert champion == from_get_champion


def test_searchable_champion_names():
    champions = cassiopeia.get_champions(region="NA")

    names = [champion.name for champion in champions]
    for name in names:
        champion = champions.find(name)
        assert champion.name == name
        champion = champions[name]
        assert champion.name == name


def test_release_dates():
    champions = cassiopeia.get_champions(region="NA")
    for champion in champions:
        champion.release_date
