[![Documentation Status](https://readthedocs.org/projects/cassiopeia/badge/?version=v3-development)](http://cassiopeia.readthedocs.org/en/v3-development/)
# Cassiopeia

A Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/).

Cassiopeia is the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application. There's two main entry points - riotapi and baseriotapi. The former handles a ton of stuff behind the scenes to make your development experience awesome, while the latter allows you fine-grained control by exposing the Riot API exactly as the website's documentation specifies.

## Documentation and Examples
Cassiopeia has detailed [documentation](http://cassiopeia.readthedocs.org/en/v3-development/) and [examples](https://github.com/meraki-analytics/cassiopeia/tree/v3-development/examples).

## Installation
`pip install cassiopeia` or see [here](<http://cassiopeia.readthedocs.io/en/v3-development/setup.html>) for more information.

## Usage

Here's an example of a basic use of the API. The full documentation can be found at http://cassiopeia.readthedocs.org/en/v3-development/.

```python
import random

import cassiopeia as cass

summoner = cass.get_summoner(name="Kalturi")
print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                          level=summoner.level
                                                                          region=summoner.region))

champions = cass.get_champions()
random_champion = random.choice(champions)
print("He enjoys playing champions such as {name}.".format(name=random_champion.name))

challenger_league = cass.get_challenger()
best_na = challenger_league[0].summoner
print("He's not as good {name} at League, but probably a better python programmer!".format(name=best_na.name))
```

## Questions/Contributions
Feel free to send pull requests or to contact us via github or [discord](https://discord.gg/uYW7qhP). More information can be found in our [documentation](http://cassiopeia.readthedocs.org/en/v3-development/).

## Bugs
If you find bugs please let us know via an issue or pull request. If you would like to help maintain Cassiopeia, let us know and we will invite you to our discord server.

## Disclaimer
Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.