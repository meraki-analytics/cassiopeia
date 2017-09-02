.. _datapipeline:

Data Pipeline
#############

The data pipeline is a fundamental piece of Cass. It controls the flow of data into and out of an in-memory cache, your databases, the Riot API, and any other data sources/sinks you provide.

The data pipeline consists of a list of ``DataSource``s and ``DataSink``s. A ``DataSource`` is any entity that *provides* data (for example, the Riot API and databases are both data sources). A ``DataSink`` is any entity that *stores* data (databases are also data sinks). Any entity that is a data sink will almost certainly be a data source as well. We refer to an entity that is both a data source and data sink as a data *store*.

The data sources and sinks are *ordered* in the data pipeline, and their order determines the order in which data is requested. Generally speaking, slower data stores / sinks should go towards the end of the pipeline.

For example, if your data pipeline consists of a cache, a database, and the Riot API (in that order), when you ask for a ``Champion`` Cassiopeia will first look in the cache, then in your database, then in the Riot API. If the data is found in the cache, it will be returned and the database and Riot API will not be queried. Similarly, if the data is found in the database, the Riot API will not be queried.

After data is found in a data source, the data propagates back down the data pipeline from whence it came. Any data sink encountered along the way will store that data. So, continuing the above example, if you asked for a ``Champion`` and it was provided by the Riot API, the champion data would be stored in your database, then stored in the cache. A data sink will only store data that it "accepts". Cass's built-in data sinks accept all of Cass's data types.

(Not yet implemented) Each data sink has expiration periods defined for each type of data it accepts. When data is put into a data sink, a clock starts ticking (metaphorically, programmatically this is handled differently). When that clock finishes, the data is expelled from the data sink. Static data should have an infinite expiration period (because it is stored per-version, and the static data for a given version never changes). Other types like ``CurrentMatch`` might have very short expiration periods. Each data sink defines the default expiration periods below.


Defining Components in your Settings
====================================

The components of the data pipeline are defined explicitly below, and you can choose which you want to use by setting the ``"pipelines"`` attribute in your settings. By default, Cass uses the in-memory cache, data dragon, and the Riot API.

Each component has it's own set of parameters, also described below.

At the end of this page is an example data pipeline you can use in your settings if you want to modify the defaults.

Components
==========

In-Memory Cache
"""""""""""""""

The in-memory cache, simply called the cache, is a data store and provides fast read / write storage of data. It is used by including ``Cache`` in the data pipeline settings. If you are constantly creating the same data over and over, the cache is extremely useful. However, if you only using pulling a given piece of data once, it is likely unnecessary.

The cache should be the first element in your pipeline.

It takes no parameters (i.e. ``{}``).


Data Dragon
"""""""""""

Data Dragon is a data source and provides all of Cass's static data. This is largely due to the static data rate limits enforced by the Riot API. If you are testing your app and running it repeatedly without a database, you will need to continuously request the static data and will quickly hit the Riot API's rate limits. Data Dragon provides exactly the same data without some of the niceties that the Riot API provides.

Data Dragon should therefore come before the Riot API in your pipeline, but likely after your databases.

It takes no parameters (i.e. ``{}``).

Riot API
""""""""

Hopefully you already know what this is. It's where you're planning on getting your data, and it's a data source. It should come after your data bases, and will likely always be the last thing in your data pipeline.

This component can have complicated settings, so see :ref:`settings` for its parameters.

Simple Disk Database
""""""""""""""""""""

This is a simple filesystem database, and is therefore both a data source and data sink. It is not provided by Cass by default, and needs to be installed separately. See :ref:`plugins` for more information.

The simple disk store takes no parameters except it's package location, which is ``cassiopeia-datastores.diskstore``.


ChampionGG
""""""""""

The ChampionGG plugin has its own data source if it is included. See :ref:`plugins`.


Example Data Pipeline Settings
==============================

.. code-block:: json

    {
      "pipeline": {
        "Cache": {},

        "SimpleKVDiskStore": {
          "package": "cassiopeia-datastores.diskstore"
        },

        "DDragon": {},

        "RiotAPI": {
          "api_key": "RIOT_API_KEY"
        },

        "ChampionGG": {
          "package": "cassiopeia-plugins.championgg",
          "api_key": "CHAMPIONGG_KEY"
        }
    }
