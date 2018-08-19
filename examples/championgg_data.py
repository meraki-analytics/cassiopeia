"""
This example requires a champion.gg api key.

You must also enable the champion.gg plugin by putting it in your settings file.

The default settings file is in `cassiopeia/configuration/default.json`, but you can create your own and pass it in as the first argument to this example to use a non-default settings file.

To enable the champion.gg plugin, add it to the data pipeline in your settings file:

  "pipline": {
    ...,
    "ChampionGG": {
      "package": "cassiopeia_championgg",
      "api_key": "CHAMPIONGG_KEY"
    },
    ...
  }

where `"CHAMPIONGG_KEY"` should be replaced with your champion.gg api key or with an environment variable containing it.
"""

import cassiopeia as cass
from cassiopeia import Champion, Role

config = cass.get_default_config()
config["pipeline"]["ChampionGG"] =  {
        "package": "cassiopeia_championgg",
        "api_key": "CHAMPIONGG_KEY"
    }
cass.apply_settings(config)


def get_champions():
    lux = Champion(name="Lux", id=99, region="NA")
    print(lux.name)

    print(lux.championgg.elo)
    print(lux.championgg.patch)

    # Lux mid vs. Lux support win rates
    print(lux.championgg[Role.middle].win_rate)
    print(lux.championgg[Role.support].win_rate)

    # Print a bunch of data
    print(lux.championgg[Role.support].play_rate)
    print(lux.championgg[Role.support].play_rate_by_role)
    print(lux.championgg[Role.support].ban_rate)
    print(lux.championgg[Role.support].games_played)
    print(lux.championgg[Role.support].damage_composition)
    print(lux.championgg[Role.support].kills)
    print(lux.championgg[Role.support].total_damage_taken)
    print(lux.championgg[Role.support].neutral_minions_killed_in_team_jungle)
    print(lux.championgg[Role.support].assists)
    print(lux.championgg[Role.support].neutral_minions_killed_in_enemy_jungle)
    print(lux.championgg[Role.support].gold_earned)
    print(lux.championgg[Role.support].deaths)
    print(lux.championgg[Role.support].minions_killed)
    print(lux.championgg[Role.support].total_healed)

    # Get matchup data for Lux mid
    # (This takes a minute to run the first time but is ~ instantaneous thereafter)
    for matchup in lux.championgg[Role.middle].matchups:
        if matchup.nmatches > 100:
            print(f"{matchup.enemy.champion.name}: {round(matchup.winrate*100)}%   ({matchup.nmatches} matches analyzed)")

if __name__ == "__main__":
    get_champions()
