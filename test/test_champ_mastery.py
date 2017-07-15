import cassiopeia

from merakicommons.container import SearchableList


def test_masteries_correct_type():
    champ_masteries = cassiopeia.get_champion_masteries('Kalturi')

    assert isinstance(champ_masteries, SearchableList)
    assert all(isinstance(cm, cassiopeia.ChampionMastery) for cm in champ_masteries)


