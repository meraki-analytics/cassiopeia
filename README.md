[![Build Status](https://circleci.com/gh/robrua/cassiopeia.svg?&style=shield&circle-token=8fb4f828f5c737e349cfb622eac18cc32fdde126)](https://circleci.com/gh/robrua/cassiopeia)[![Documentation Status](https://readthedocs.org/projects/cassiopeia/badge/?version=latest)](http://cassiopeia.readthedocs.org/en/latest/?badge=latest)
# Cassiopeia

A Python 3 adaptation of the Riot Games LoL API (https://developer.riotgames.com/).

Cassiopeia is the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application. There's two main entry points - riotapi and baseriotapi. The former handles a ton of stuff behind the scenes to make your development experience awesome, while the latter allows you fine-grained control by exposing the Riot API exactly as the website's documentation specifies.

## Features (riotapi)

- Usability-focused type system to make your life easy
- Automatically throttles requests to fit rate limits
- Ensures well-formed API requests
- Replaces foreign key ID values with the referenced object
- Option to lazy load referenced objects right when you need them or batch them up and eagerly load them to minimize API calls
- Caches static data and summoner information to accelerate access and reduce API load
- Available automatic databasing using [SQLAlchemy](http://www.sqlalchemy.org/)

## Features (baseriotapi)

- Meets the Riot API specification exactly
- Automatically throttles requests to fit rate limits
- Ensures well-formed API requests
- Make only the requests you want to make, no foreign keys are auto-filled
 
## Setup

Just `pip install cassiopeia` and you're good to go!

If you want to reference to most recent codebase from github to stay up to date with every single change, download the code from github and add the root directory (the one that contains LICENSE.txt) or the .zip file to your PYTHONPATH environment variable.

## Dependencies

Cassiopeia depends on [SQLAlchemy](http://www.sqlalchemy.org/). It should be automatically installed for you if you install with pip. Otherwise, do `pip install sqlalchemy`.
 
## Usage

Here's an example of a few basic uses of the API. The full documentation can be found at http://cassiopeia.readthedocs.org/en/latest/.

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

Make sure you set your rate limit! Cassiopeia will limit you the the default development limit until you give it your production limit (if you have one).

```python
# 3,000 calls per 10 seconds
riotapi.set_rate_limit(3000, 10);
# 3,000 calls per 10 seconds AND 180,000 calls per 10 minutes
riotapi.set_rate_limits((3000, 10), (180000, 600))
```

You can also set a load policy for filling in foreign key values to optimize internal call usage. Eager will load everything ASAP, and will batch together calls where possible to minimize call usage. Lazy will load things as you ask for them, so you can save calls if you don't use some values, but it won't be able to take as much advantage of bulk loading.

```python
from cassiopeia.type.core.common import LoadPolicy

# Eager loading is the default strategy
riotapi.set_load_policy(LoadPolicy.eager)
riotapi.set_load_policy(LoadPolicy.lazy)
```

Or, if you don't want all the bells and whistles and you'd just like to access the Riot API as the specification says, you can use baseriotapi.

```python
import random

from cassiopeia import baseriotapi

baseriotapi.set_region("NA")
baseriotapi.set_api_key("YOUR-API-KEY-HERE")

summoner = baseriotapi.get_summoners_by_name("FatalElement")["fatalelement"]
print("{name} is a level {level} summoner on the NA server.".format(name=summoner.name, level=summoner.summonerLevel))

champions = baseriotapi.get_champions()
random_champion = random.choice(list(champions.data.values()))
print("He enjoys playing LoL on all different champions, like {name}.".format(name=random_champion.name))

challenger_league = baseriotapi.get_challenger("RANKED_SOLO_5x5")
a_challenger = challenger_league.entries[0].playerOrTeamName
print("He's much better at writing Python code than he is at LoL. He'll never be as good as {name}.".format(name=a_challenger))
```

## Running tests

After cloning the repo:

```bash
pip install -r requirements.txt
```

Then
```bash
py.test
```

## Documentation
[Found Here](http://cassiopeia.readthedocs.org/en/latest/)

## Download
[Releases](https://github.com/robrua/cassiopeia/releases)

## Questions/Contributions
Feel free to send pull requests or to contact me via github or email (robrua@alumni.cmu.edu).

## Bugs
There's probably typos or some data missing somewhere in the project. Let me know about any of them you run into. I'm also looking for consistent maintainers to help me out as the Riot API evolves.

## Disclaimer
Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
