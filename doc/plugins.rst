.. _plugins:

Plugins
#######

Plugins monkeypatch Cass to provide modified or additional functionality. They are listed below.

The plugins for Cass are stored in two different repositories: `cassiopeia-plugins <https://github.com/meraki-analytics/cassiopeia-plugins>`_ and `cassiopeia-datastores <https://github.com/meraki-analytics/cassiopeia-datastores>`_. ``cassiopeia-plugins`` contains functionality that modify the behavior of Cass's objects, while ``cassiopeia-datastores`` provides additional datastores (such as databases). Both of these are called "plugins" in this documentation.

Plugins can be added to Cass by downloading the appropriate plugin and putting it on your ``PYTHONPATH`` environment variable. Then, in your settings file, you specify the relative path to that plugin (using the ``package`` keyword) as if you were directly importing it into your project. The name of the package specifies the data store that that will be loaded from that package and put on the pipeline.


ChampionGG
----------

The ChampionGG plugin pulls data from the `champion.gg api <http://api.champion.gg>`_ . This data is accessible via the ``Champion.championgg`` attribute.

To enable this plugin, add the following to your settings' data pipeline:

.. code-block:: json

  "pipline": {
    ...,
    "ChampionGG": {
      "package": "cassiopeia-plugins.championgg.championgg",
      "api_key": "CHAMPIONGG_KEY"
    },
    ...
  }

where ``"CHAMPIONGG_KEY"`` is your champion.gg API key or an environment variable that contains it.


Simple KV Disk Store
--------------------

This plugin provides a disk-database. It is especially useful for staticdata, which never changes. It works for all data types except ``MatchHistory``.

To enable this plugin, add the following to your settings' data pipeline between the ``Cache`` and ``DDragon`` stores:

.. code-block:: json

  "pipline": {
    ...,
    "SimpleKVDiskStore": {
      "package": "cassiopeia-datastores.diskstore.diskstore",
      "path": "/absolute/path/to/store/data/"
    },
    ...
  }
