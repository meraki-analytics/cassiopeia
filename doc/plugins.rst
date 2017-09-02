.. _plugins:

Plugins
#######

Plugins monkeypatch Cass to provide modified or additional functionality. They are listed below.

Champion GG
-----------

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
      "package": "cassiopeia-datastores.diskstore.diskstore"
    },
    ...
  }
