.. _plugins:

Plugins
#######

Plugins monkeypatch Cass to provide modified or additional functionality. They are listed below.

The plugins for Cass are stored in two different repositories: `cassiopeia-plugins <https://github.com/meraki-analytics/cassiopeia-plugins>`_ and `cassiopeia-datastores <https://github.com/meraki-analytics/cassiopeia-datastores>`_. ``cassiopeia-plugins`` contains functionality that modify the behavior of Cass's objects, while ``cassiopeia-datastores`` provides additional datastores (such as databases). Both of these are called "plugins" in this documentation.

Plugins can be added to Cass by downloading the appropriate plugin and putting it on your ``PYTHONPATH`` environment variable. Then, in your settings file, you specify the name of the module for that plugin (using the ``package`` keyword) as if you were directly importing it into your project. The name of the package specifies the data store that that will be loaded from that package and put on the pipeline.


ChampionGG
----------

Install by running ``pip install cassiopeia-championgg``.

The ChampionGG plugin pulls data from the `champion.gg api <http://api.champion.gg>`_ . This data is accessible via the ``Champion.championgg`` attribute.

To enable this plugin, add the following to your settings' data pipeline:

.. code-block:: json

  "pipeline": {
    ...,
    "ChampionGG": {
      "package": "cassiopeia_championgg",
      "api_key": "CHAMPIONGG_KEY"
    },
    ...
  }

where ``"CHAMPIONGG_KEY"`` is your champion.gg API key or an environment variable that contains it.


Simple KV Disk Store
--------------------

Install by running ``pip install cassiopeia-diskstore``.

This plugin provides a disk-database. It is especially useful for staticdata, which never changes. It works for all data types except ``MatchHistory``.

To enable this plugin, add the following to your settings' data pipeline between the ``Cache`` and ``DDragon`` stores:

.. code-block:: json

  "pipeline": {
    ...,
    "SimpleKVDiskStore": {
      "package": "cassiopeia_diskstore",
      "path": "/absolute/path/to/store/data/"
    },
    ...
  }

The ``"path"`` parameter specifies a directory path where the data will be stored. There is also another optional ``"expirations"`` parameter that is left out of the above example for clarity. The ``"expirations"`` parameter is a mapping of type names to expiration periods analogous to those for the cache. The allowed type names and default values are below (a value of ``-1`` means "do not expire" and ``0`` means "do not store in the data sink):

.. code-block:: python

    RealmDto: datetime.timedelta(hours=6),
    VersionListDto: datetime.timedelta(hours=6),
    ChampionDto: -1,
    ChampionListDto: -1,
    RuneDto: -1,
    RuneListDto: -1,
    ItemDto: -1,
    ItemListDto: -1,
    SummonerSpellDto: -1,
    SummonerSpellListDto: -1,
    MapDto: -1,
    MapListDto: -1,
    ProfileIconDetailsDto: -1,
    ProfileIconDataDto: -1,
    LanguagesDto: -1,
    LanguageStringsDto: -1,
    ChampionRotationDto: datetime.timedelta(days=1),
    ChampionMasteryDto: datetime.timedelta(days=7),
    ChampionMasteryListDto: datetime.timedelta(days=7),
    ShardStatusDto: datetime.timedelta(hours=1),

Some objects share the same expiration time: ``FeaturedGamesDto`` shares expiration of ``CurrentGameInfoDto``, ``ChallengerLeagueListDto`` and ``MasterLeagueListDto`` share expiration of ``LeagueListDto``, ``ChampionMasteryListDto`` shares expiration of ``ChampionMasteryDto``, and ``ChampionListDto`` shares expiration of ``ChampionDto``. Only the latter in each category need to be set.

This store only supports the above types (for now).
