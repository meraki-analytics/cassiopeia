.. _plugins:

Plugins
#######

Plugins monkeypatch Cass to provide modified or additional functionality. They are listed below.

Champion GG
-----------

The Champion GG plugin pulls data from the `champion.gg api <http://api.champion.gg>`_ . This data is accessible via the ``Champion.championgg`` attribute.

To enable this plugin, add the following json to your settings' plugins:

.. code-block:: json

    "championgg": {
      "key": "CHAMPIONGG_KEY"
    }

where ``"CHAMPIONGG_KEY"`` is your champion.gg API key or an environment variable that contains it.
