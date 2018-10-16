import cassiopeia


def test_rotation_data():
    rotation = cassiopeia.get_champion_rotations(region="NA")
    assert 1 <= rotation.max_new_player_level <= 30

    rotation = cassiopeia.ChampionRotation(region="NA")
    assert 1 <= rotation.max_new_player_level <= 30
