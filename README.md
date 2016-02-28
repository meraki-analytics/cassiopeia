[![Documentation Status](https://readthedocs.org/projects/cassiopeia/badge/?version=latest)](http://cassiopeia.readthedocs.org/en/latest/)
# Cassiopeia

A Python adaptation of the Riot Games LoL API (https://developer.riotgames.com/).

Cassiopeia is the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application. There's two main entry points - riotapi and baseriotapi. The former handles a ton of stuff behind the scenes to make your development experience awesome, while the latter allows you fine-grained control by exposing the Riot API exactly as the website's documentation specifies.

## Documentation
[Found Here](http://cassiopeia.readthedocs.org/en/latest/)

## Download
[Releases](https://github.com/robrua/cassiopeia/releases)

## Usage

Here's an example of a basic use of the API. The full documentation can be found at http://cassiopeia.readthedocs.org/en/latest/.

```python
import random

from cassiopeia import riotapi

riotapi.set_region("NA")
riotapi.set_api_key("YOUR-API-KEY-HERE")

summoner = riotapi.get_summoner_by_name("FatalElement")
print("{name} is a level {level} summoner on the NA server.".format(name=summoner.name, level=summoner.level))

champions = riotapi.get_champions()
random_champion = random.choice(champions)
print("He enjoys playing LoL on all different champions, like {name}.".format(name=random_champion.name))

challenger_league = riotapi.get_challenger()
best_na = challenger_league[0].summoner
print("He's much better at writing Python code than he is at LoL. He'll never be as good as {name}.".format(name=best_na.name))
```

## Questions/Contributions
Feel free to send pull requests or to contact us via github or email (team@merakianalytics.com, robrua@alumni.cmu.edu, or jjmaldonis@gmail.com).

## Bugs
If you find bugs please let us know via an issue or pull request. If you would like to help maintain Cassiopeia, let us know and we will invite you to our slack group.

## Disclaimer
Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
