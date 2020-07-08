Using Cassiopeia
================

Objects that hold data from the Riot API can be created using two different interfaces. The top-level ``cassiopeia`` module contains methods to query for objects using method calls, as well as class constructors to create objects directly.

Example usage of the two interfaces:

.. code-block:: python

    import cassiopeia as cass
    kalturi = cass.get_summoner(name="Kalturi", region="NA")

    from cassiopeia import Summoner
    kalturi = Summoner(name="Kalturi", region="NA")

Also note that many types can be pulled from ``Summoner`` objects. This is the preferred way to interact with these types. They are listed below:

.. code-block:: python

    from cassiopeia import Summoner
    kalturi = Summoner(name="Kalturi", region="NA")
    kalturi.champion_masteries
    kalturi.match_history
    kalturi.current_match
    kalturi.leagues
    
Django web Framework
--------------------
There is an integration of cassiopeia to the popular python web framework Django made by Mori(Paaksing), this integration is aimed to fix most issues/conflicts that happens when Cassiopeia is paired with a Python web framework (e.g. Django, Flask). In this integration, you will have the ability to use any production tested cache backends that Django's cache framework supports (Memcached, Redis, Filebased, Locmem, Database/SQL, etc), plus others well adapted settings.

* Link to `django-cassiopeia` [repository](https://github.com/paaksing/django-cassiopeia) (If you love using it, make sure to star!).
* Link to `django-cassiopeia` [documentations](https://django-cassiopeia.readthedocs.io/en/latest/) (A dark theme is added to save you some eyeballs).
* If you have any issues or feature requests with `django-cassiopeia`, tag Mori in our discord server, or fire an issue in the repository.

Unfortunately, we currently don't have an integration to Flask and any contribution is welcome.


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
