.. _inner-workings:

Contributing
============

There are a few major parts that make Cass work, with minor parts that go along with them. These are discussed below.


Major Parts
-----------

Two Interfaces
""""""""""""""

Cass has two interfaces that work nearly identically. Depending on your coding style, you can choose the one that you prefer. One uses ``.get_...`` methods to get objects, while the other prefers constructors to create objects. Both are equally good. For example, ``cass.get_summoner(name="Kalturi")`` and ``Summoner(name="Kalturi")`` both work.


Settings
""""""""

There are a few settings in Cass that should be modified, and more that can. We provide default settings in the file ``cassiopeia/configuration/default.ini``.

Most importantly, your API key should be set. You can set this by providing the key itself, or by providing the name of an environment variable that contains your API key. We encourage you to put your API key in an environment variable, but if you put your API key in the file just be careful not to push it to version control.

A default region can be set in the settings, and any object that requires a region but isn't provided when during initialization will use the default region.

(Not yet implemented) All Cass objects have expiration timeouts that can be modified. See the :ref:`Data Pipeline <data-pipeline>` section below.


Ghost Loading
"""""""""""""

A *ghost object* is an object that can be instantiated without all of its data. It is therefore a shadow of itself, or a *ghost*. Ghost objects know how to load the rest of their data using what they were given at init. This is what allows you to write `kalturi = Summoner(name="Kalturi")` followed by `kalturi.level`. The latter makes a call to the data pipeline (discussed below) to pull the rest of the data for `kalturi` by using `kalturi.name`.

All top-level objects in Cass are ghost objects and therefore know how to load their own data.

The implementation for ghost objects can be found in our Meraki Commons repository on GitHub.


.. _data-pipeline:

Data Pipeline
"""""""""""""

The data pipeline is the series of caches, databases, and data sources (such as the Riot API) that both provide and store data. Some parts of the pipeline are just data sources (the Riot API), while many are both data sources and data sinks (caches and databases). Data sources provide data, while data sinks store data. The sources and sinks in the data pipeline are in a specific order, usually with faster data sources at the beginning and slower ones at the end.

When data is queried, a query dictionary is constructed containing the information needed to uniquely identify an object in a data source (e.g. a ``region`` and ``summoner.id`` are required when querying for ``Summoner`` objects). The query is passed up the data pipeline through the data sources, and at each data source the data pipeline asks if that source has the object corresponding to the query. If the source does contain the object, it is returned. If the source does not contain the object, the next data source in the pipeline is queried. If no data source can provide an object for the query, a `datapipelines.NotFoundError` is thrown.

After an object is returned by a data source, the object gets passed back down the pipeline. An data sinks along the way store the object that was returned by the data source. In this way, the cache (which should be at the front of the data pipeline) will store any object that a database or the Riot API returned.

A data pipeline containing an in-memory cache and the Riot API is created by default. The pipeline can be accessed via `settings.pipeline`, although users should rarely if ever touch this object.

(Not yet implemented) Expiration times for objects are allowed. If an object in a data sink expires, it will be removed from the data sink. This happens periodically when data is queried. Users can force all expired objects in data sinks to be removed using `settings.pipeline.expire()`.
