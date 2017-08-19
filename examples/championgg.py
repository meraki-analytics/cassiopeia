from cassiopeia import Champion


def get_champions():
    annie = Champion(name="Annie", id=1, region="NA")
    print(annie.name)

    print(annie.win_rate)
    print(annie.play_rate)
    print(annie.play_percent)
    print(annie.ban_rate)
    print(annie.games_played)
    print(annie.damage_composition)
    print(annie.kills)
    print(annie.total_damage_taken)
    print(annie.wards_killed)
    print(annie.neutral_minions_killed_in_team_jungle)
    print(annie.assists)
    print(annie.performance_score)
    print(annie.neutral_minions_killed_in_enemy_jungle)
    print(annie.gold_earned)
    print(annie.deaths)
    print(annie.minions_killed)
    print(annie.total_healed)
    print(annie.championgg_metadata["elo"])
    print(annie.championgg_metadata["patch"])



if __name__ == "__main__":
    get_champions()
