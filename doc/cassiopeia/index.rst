Using Cassiopeia
================

Objects that hold data from the Riot API can be created using two different interfaces. The top-level ``cassiopeia`` module contains methods to query for objects using method calls, as well as class constructors to create objects directly.

Example usage of the two interfaces:

.. code-block:: python

    import cassiopeia as cass
    a_summoner = cass.get_summoner(puuid="...", region="NA")

    from cassiopeia import Summoner
    a_summoner = Summoner(puuid="...", region="NA")

Also note that many types can be pulled from ``Summoner`` objects. This is the preferred way to interact with these types. They are listed below:

.. code-block:: python

    from cassiopeia import Summoner
    a_summoner = Summoner(puuid="...", region="NA")
    a_summoner.champion_masteries
    a_summoner.match_history
    a_summoner.current_match
    a_summoner.leagues
    

Methods and Class Constructors
------------------------------

See the links below for the method and class names for each type.

.. toctree::

    settings.rst
    data.rst
    champion.rst
    championmastery.rst
    item.rst
    languagestrings.rst
    league.rst
    locale.rst
    map.rst
    match.rst
    patch.rst
    profileicon.rst
    realms.rst
    rune.rst
    shard.rst
    spectator.rst
    summoner.rst
    summonerspell.rst
    versions.rst
