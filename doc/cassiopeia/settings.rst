Settings
########

That are many settings in Cassiopeia that control how the framework works, and more settings will be added as the code is expanded.

The most important settings are the Riot API key and the default region. Both of these can be set programmatically, but it is often easiest to just change your settings file instead. Please see ``cassiopeia/configuration/default.json`` for an up to date example of a settings file.

Each setting is explained below, and should be added as separate entries to the settings file (which is in ``json`` format).

Riot API
""""""""

The ``"Riot API"`` section defines variable relevant to the Riot API.

The ``"region"`` should be set to the string version of the region that the Riot API requires (in all caps), for example ``"NA"`` for North America.

The ``"key"`` should be set to your Riot API key. You can instead supply an environment variable name that contains your API key (this is recommended so that you can push your settings file to version control without revealing your API key).

Example:

.. code-block:: json

    "Riot API": {
        "region": "NA",
        "key": "RIOT_API_KEY"
    }


Logging
"""""""

The ``"logging"`` section defines variables related to logging and print statements.

The ``"print_calls"`` variable should be set to ``true`` or ``false`` and determines whether http calls (e.g. to the Riot API or Data Dragon) are printed.

``"core"`` and ``"default"`` are two loggers that are currently implemented in Cass, and you can set the logging levels using these variables. Acceptable values are the logging levels for python's logging module (e.g. ``"INFO"`` and ``"WARNING"``).

Example:

.. code-block:: json

    "logging": {
        "print_calls": true,
        "default": "WARNING",
        "core": "WARNING"
    }

Plugins
"""""""

The ``"plugins"`` section defines which plugins Cassiopeia will use. See :ref:`plugins` for specifics for each plugin.

Example:

.. code-block:: json

    "plugins": {
        "championgg": {
            ...
        }
    }
