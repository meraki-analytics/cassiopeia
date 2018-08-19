[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/meraki-analytics/orianna/blob/master/LICENSE.txt)
[![Documentation Status](https://readthedocs.org/projects/cassiopeia/badge/?version=latest)](http://cassiopeia.readthedocs.org/en/latest/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1170906.svg)](https://doi.org/10.5281/zenodo.1170906)

# Cassiopeia

A Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/).

Cassiopeia is the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application.


## Documentation and Examples
Cassiopeia has detailed [documentation](http://cassiopeia.readthedocs.org/en/latest/) and [examples](https://github.com/meraki-analytics/cassiopeia/tree/master/examples).


## Installation
`pip install cassiopeia` or see [here](<http://cassiopeia.readthedocs.io/en/latest/setup.html>) for more information.


## Why use Cass?

* An excellent user interface that makes working with data from the Riot API easy and fun.

* "Perfect" rate limiting.

* Guaranteed optimal usage of your API key.

* Built in caching and (coming) the ability to easily hook into a database for offline storage of data.

* Extendability to non-Riot data. Because Cass is a framework and not just an API wrapper, you can integrate your own data sources into your project. Cass already supports Data Dragon and the ``champion.gg`` API in addition to the Riot API.

* Dynamic settings so you can configure Cass for your specific use case.


## Example

Here's an example of a basic use of the API. The full documentation can be found at http://cassiopeia.readthedocs.org/en/latest/.

```python
import random

import cassiopeia as cass

cass.set_riot_api_key("YOUR_KEY")  # This overrides the value set in your configuration/settings.
cass.set_default_region("NA")

summoner = cass.get_summoner(name="Kalturi")
print("{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                          level=summoner.level,
                                                                          region=summoner.region))

champions = cass.get_champions()
random_champion = random.choice(champions)
print("He enjoys playing champions such as {name}.".format(name=random_champion.name))

challenger_league = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives)
best_na = challenger_league[0].summoner
print("He's not as good as {name} at League, but probably a better python programmer!".format(name=best_na.name))
```


## Questions/Contributions
Feel free to send pull requests or to contact us via github or [discord](https://discord.gg/uYW7qhP). More information can be found in our [documentation](http://cassiopeia.readthedocs.org/en/latest/).


## Bugs
If you find bugs please let us know via an issue or pull request. If you would like to help maintain Cassiopeia, let us know and we will invite you to our discord server.

## Citing Cassiopeia
If you used Cassiopeia for your research, please [cite the project](https://doi.org/10.5281/zenodo.1170906).

## Support Us
If you've loved using Cassiopeia, consider supporting us through [PayPal](https://www.paypal.me/merakianalytics) or [Patreon](https://www.patreon.com/merakianalytics).

## Disclaimer
Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
