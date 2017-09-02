"""
This example requires a champion.gg api key.

You must also enable the champion.gg plugin by putting it in your settings file.

The default settings file is in `cassiopeia/configuration/default.json`, but you can create your own and pass it in as the first argument to this example to use a non-default settings file.

To enable the champion.gg plugin, add it to the plugins in your settings file:

  "plugins": {
    "championgg": {
      "key": "CHAMPIONGG_API_KEY"
    }
  }

where `"CHAMPIONGG_API_KEY"` should be replaced with your champion.gg api key or with an environment variable containing it.
"""

from cassiopeia import Champion


def get_champions():
    annie = Champion(name="Annie", id=1, region="NA")
    print(annie.name)

    print(annie.championgg.win_rate)
    print(annie.championgg.play_rate)
    print(annie.championgg.play_rate_by_role)
    print(annie.championgg.ban_rate)
    print(annie.championgg.games_played)
    print(annie.championgg.damage_composition)
    print(annie.championgg.kills)
    print(annie.championgg.total_damage_taken)
    print(annie.championgg.wards_killed)
    print(annie.championgg.neutral_minions_killed_in_team_jungle)
    print(annie.championgg.assists)
    print(annie.championgg.performance_score)
    print(annie.championgg.neutral_minions_killed_in_enemy_jungle)
    print(annie.championgg.gold_earned)
    print(annie.championgg.deaths)
    print(annie.championgg.minions_killed)
    print(annie.championgg.total_healed)
    print(annie.championgg.championgg_metadata["elo"])
    print(annie.championgg.championgg_metadata["patch"])


if __name__ == "__main__":
    get_champions()
