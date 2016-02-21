Basic Usage
###########

Below is a basic example illustrating how to use Cassiopeia. The code starts by importing the core of Cassiopeia, ``riotapi``, which is used to pull data from the Riot API.

Next, the region and api key are set (you will need to input your own api key here).

The ``get_summoner_by_name`` method is then called to pull summoner information from the Summoner endpoint for FatalElement (the creator of this library). His summoner name and level are accessed and printed to screen.

In a similar manner, the ``get_champions`` and ``get_challenger`` methods are called to get data for every champion and to get the list of all summoners in the Challenger tier.

.. code-block:: python

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

You can find more examples within Cassiopeia's `examples <https://github.com/meraki-analytics/cassiopeia/tree/master/example>`_ directory.


More Examples
=============

* `Getting Champion Names and IDs <https://github.com/meraki-analytics/cassiopeia/blob/master/example/champion_id_to_name_mapping.py>`_
* `Calculating K/D/A <https://github.com/meraki-analytics/cassiopeia/blob/master/example/calculate_average_kda.py>`_
* `Checking if a Summoner is in Game <https://github.com/meraki-analytics/cassiopeia/blob/master/example/is_dyrus_in_game.py>`_
* `Accessing Lane and Role Information from a Match <https://github.com/meraki-analytics/cassiopeia/blob/master/example/lane_and_role_from_match.py>`_
* `Accessing More Match Data <https://github.com/meraki-analytics/cassiopeia/blob/master/example/parse_match_information.py>`_
* `Working with Dates and Times <https://github.com/meraki-analytics/cassiopeia/blob/master/example/time_and_date_info.py>`_
* `Pull All Summoners in the Master Tier <https://github.com/meraki-analytics/cassiopeia/blob/master/example/pull_masters_tier.py>`_
* `Advanced: Recursive Match Collection <https://github.com/meraki-analytics/cassiopeia/blob/master/example/match_collection.py>`_
