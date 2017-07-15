import cassiopeia
import pytest

from merakicommons.container import SearchableList
from datapipelines.common import NotFoundError


def test_masteries_correct_type():
    champ_masteries = cassiopeia.get_champion_masteries('Kalturi')

    assert isinstance(champ_masteries, SearchableList)
    assert all(isinstance(cm, cassiopeia.ChampionMastery) for cm in champ_masteries)


def test_raises_with_unknown_summoner():
    with pytest.raises(NotFoundError):
        cassiopeia.get_champion_masteries('abcaklsjdlaksdjlaksjdla')


def test_masteries_with_id_or_summoner():
    summ = cassiopeia.get_summoner('Kalturi')

    from_summoner = cassiopeia.get_champion_masteries(summ)
    from_id = cassiopeia.get_champion_masteries(summ.id)
    from_name = cassiopeia.get_champion_masteries(summ.name)

    assert from_summoner == from_id
    assert from_id == from_name
