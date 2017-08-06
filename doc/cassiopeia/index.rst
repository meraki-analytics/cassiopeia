Using Cassiopeia
================

Objects that hold data from the Riot API can be created using two different interfaces. The top-level ``cassiopeia`` module contains methods to query for objects using method calls, as well as class constructors to create objects directly.

Example usage of the two interfaces:

.. code-block:: python

    import cassiopeia as cass
    kalturi = cass.get_summoner(name="Kalturi")

    from cassiopeia import Summoner
    kalturi = Summoner(name="Kalturi")

Also note that many types can be pulled from ``Summoner`` objects. This is the preferred way to interact with these types. They are listed below:

.. code-block:: python

    from cassiopeia import Summoner
    kalturi = Summoner(name="Kalturi")
    kalturi.champion_masteries
    kalturi.match_history
    kalturi.mastery_pages
    kalturi.rune_pages
    kalturi.current_match
    kalturi.leagues


Methods and Class Constructors
------------------------------

See on the links below for the method and class names for each type.

.. toctree::

    champion.rst
    championmastery.rst
    item.rst
    languagestrings.rst
    league.rst
    locale.rst
    map.rst
    mastery.rst
    match.rst
    profileicon.rst
    realms.rst
    rune.rst
    shard.rst
    spectator.rst
    summoner.rst
    summonerspell.rst
    versions.rst


Data and Enums
--------------

These data are available as enums (constants) and can be used to interact with many of the objects and methods in Cass.

.. currentmodule:: cassiopeia

.. automodule:: cassiopeia.data
    :members:
    :undoc-members:
    :show-inheritance:


.. automodule:: cassiopeia.patches
    :members:
    :undoc-members:
    :show-inheritance:
