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
from cassiopeia import Champion
import cassiopeia_championgg

config = cass.get_default_config()
config["pipeline"]["ChampionGG"] =  {
        "package": "cassiopeia_championgg",
        "api_key": "CHAMPIONGG_KEY"
    }
cass.apply_settings(config)

from cassiopeia import RoleGG  # This gets monkey patched in by the champion.gg plugin, but we have to load it after putting ChampionGG in the pipeline


def get_champions():
    champions = cass.get_champions(region="NA")
    for champion in champions:
        print(f"{champion.name}: {[role for role in champion.championgg.roles.keys()]}")
    print()

    lux = Champion(name="Lux", id=99, region="NA")
    print(lux.name)

    print(lux.championgg.elo)
    print(lux.championgg.patch)

    # Lux mid vs. Lux support win rates
    print(lux.championgg[RoleGG.middle].win_rate)
    print(lux.championgg[RoleGG.support].win_rate)

    # Print a bunch of data
    print(lux.championgg[RoleGG.support].play_rate)
    print(lux.championgg[RoleGG.support].play_rate_by_role)
    print(lux.championgg[RoleGG.support].ban_rate)
    print(lux.championgg[RoleGG.support].games_played)
    print(lux.championgg[RoleGG.support].damage_composition)
    print(lux.championgg[RoleGG.support].kills)
    print(lux.championgg[RoleGG.support].total_damage_taken)
    print(lux.championgg[RoleGG.support].neutral_minions_killed_in_team_jungle)
    print(lux.championgg[RoleGG.support].assists)
    print(lux.championgg[RoleGG.support].neutral_minions_killed_in_enemy_jungle)
    print(lux.championgg[RoleGG.support].gold_earned)
    print(lux.championgg[RoleGG.support].deaths)
    print(lux.championgg[RoleGG.support].minions_killed)
    print(lux.championgg[RoleGG.support].total_healed)

    # Get matchup data for Lux mid
    # (This takes a minute to run the first time but is ~ instantaneous thereafter)
    for matchup in lux.championgg[RoleGG.middle].matchups:
        if matchup.nmatches > 100:
            print(f"{matchup.enemy.champion.name}: {round(matchup.winrate*100)}%   ({matchup.nmatches} matches analyzed)")

if __name__ == "__main__":
    get_champions()
