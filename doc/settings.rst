Settings
########

That are many settings in Cassiopeia that control how the framework works, and more settings will be added as the code is expanded.

The most important settings are the Riot API key and the default region. Both of these can be set programmatically, but it is often easiest to just change your settings file instead. Please see ``cassiopeia/configuration/default.json`` for an up to date example of a settings file.

Each setting is explained below, and should be added as separate entries to the settings file (which is in ``json`` format).

Riot API
--------

The ``"Riot API"`` section defines variable relevant to the Riot API.

The ``"region"`` should be set to the string version of the region that the Riot API requires (in all caps), for example ``"NA"`` for North America.

The ``"key"`` should be set to your Riot API key. You can instead supply an environment variable name that contains your API key (this is recommended so that you can push your settings file to version control without revealing your API key).

If the ``"region"`` and ``"key"`` are not set in the settings file, they should be set programmatically via ``cass.set_default_region`` and ``cass.set_riot_api_key``.

The ``"limit_sharing"`` variable specifies what fraction of your API key should be used for your server. This is useful when you have multiple servers that you want to split your API key over. The default (if not set) is ``1.0``, and valid values are between ``0.0`` and ``1.0``.

Request Handling
""""""""""""""""

The ``"request_handling"`` variable specifies how Riot API errors should be handled. There are three options, each of which have their own set of parameters: ``"throw"`` simply causes and error returned by the Riot API to be thrown to you, the user; ``"exponential_backoff"`` will exponentially backoff; and ``"retry_from_headers"`` will attempt to use the ``"retry-after"`` header in the response to retry after the specified amount of time. The ``429`` error code can be handled differently depending on which type of rate limiting cause it. See the example below for the specific structure for these settings.

``"throw"`` takes no arguments.

``"exponential_backoff"`` takes three arguments: ``initial_backoff`` specifies the initial time to pause before making another request, ``backoff_factor`` specifies what to multiply the ``initial_backoff`` by for each subsequent failure, and ``max_attempts`` specifies the maximum number of calls to make before throwing the error.

``"retry_from_headers"`` takes one argument: ``max_attempts`` specifies the maximum number of calls to make before throwing the error.

Below is an example, and these settings are the default if any value is not specified:

.. code-block:: json

    "Riot API": {
        "region": "NA",
        "key": "RIOT_API_KEY",
        "limiting_share": 1.0,
        "request_handling": {
            "404": {
                "strategy": "throw"
            },
            "429": {
                "service": {
                    "strategy": "exponential_backoff",
                    "initial_backoff": 1.0,
                    "backoff_factor": 2.0,
                    "max_attempts": 4
                },
                "method": {
                    "strategy": "retry_from_headers",
                    "max_attempts": 5
                },
                "application": {
                    "strategy": "retry_from_headers",
                    "max_attempts": 5
                }
          },
          "500": {
              "strategy": "throw"
          },
          "503": {
              "strategy": "throw"
          },
          "timeout": {
              "strategy": "throw"
          }
        }
    }


Logging
-------

The ``"logging"`` section defines variables related to logging and print statements.

The ``"print_calls"`` variable should be set to ``true`` or ``false`` and determines whether http calls (e.g. to the Riot API or Data Dragon) are printed. Similarly, the ``"print_api_key"`` variable will print your Riot API key if set to ``true``.

``"core"`` and ``"default"`` are two loggers that are currently implemented in Cass, and you can set the logging levels using these variables. Acceptable values are the logging levels for python's logging module (e.g. ``"INFO"`` and ``"WARNING"``).

Example:

.. code-block:: json

    "logging": {
        "print_calls": true,
        "default": "WARNING",
        "core": "WARNING"
    }

Plugins
-------

The ``"plugins"`` section defines which plugins Cassiopeia will use. See :ref:`plugins` for specifics for each plugin.

Example:

.. code-block:: json

    "plugins": {
        "championgg": {
            ...
        }
    }