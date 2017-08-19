.. _contributions:

Contributing
############

Contributions are welcome! If you have idea or opinions on how things can be improved, don't hesitate to let us know by posting an issue on GitHub or @ing us on the Meraki or Riot API Discord channel. And we always want to hear from our users, even (especially) if it's just letting us know how you are using Cass.

As a user you get to ignore the details and just use the features of Cass. But as a developer you get to dive into the nitty-gritty and pick apart the implementation that makes everything work. If you don't want to dive too deep, you can likely contribute even without knowing all the details. You can read more about how Cass works :ref:`here <inner-workings>`, and you can find opportunities to help by looking at our issues that are tagged with ``help-wanted`` as well as our :ref:`contributions page <contributions>`.

If you have an idea but aren't sure about it, feel free to @ us on Discord and we can chat.



Things we need help with!
-------------------------

* We current don't support the tournament API but need to.

* Very few methods / properties have doc strings. While not glorious, it is an incredibly helpful thing to do and you will quickly learning all the pieces of Cass.

* In the previous version of Cass, we used regex to pull item stats from tooltips, because the static data is missing a significant number of stats. The old code can be found `here <https://github.com/meraki-analytics/cassiopeia/blob/db8930d534e400299bf8ebb814449e101e6f6fbc/cassiopeia/type/core/staticdata.py#L251>`_ and needs to be ported to this version of Cass.

* We want to support Redis, Mongo, and SQLAlchemy. To do so, new datasources should be added (along side the Riot API and the in-memory cache) to support each of these.

* Add ``get_many_*`` functions to the ddragon data source, similar to the riotapi data source.

* Have the ddragon data source cache it's data (since its data is independent of region) and return the cached data for different regions if multiple are requested (rather than send an http request to ddragon for each region).

* We have some tests in place, but a thorough testing of all attributes of all objects would be extremely helpful.

* Some data from the `champion.gg api <http://api.champion.gg>`_ is available through Cass (via the ``Champion`` object). The remaining data should be added as well. You can find the relevant code in the ``plugins/championgg`` directory.

* Add functionality for setting ``version="latest"`` for all objects.

* Currently, the patches file needs to be updated with the correct start date every time a new patch is released. There must be some way to automate this.

* Allow a patch to be given as a ``version`` rather than a string, and therefore allow ``MatchHistory`` objects to be indexable by patch number. Version numbers (e.g. ``"7.14.2"``) are more strict than patch numbers (e.g. ``"7.14"``).

* ``Map`` and locales are approximately duplicated in two different ways. The ``Map`` class is implemented as both ``Enum`` and ``CassiopeiaGhost``, and this functionality can likely be combined in some way. Similarly, locales can be pulled using the ``Locales`` ``CassiopeiaGhost`` type, and locales should also probably be ``Enum`` s that get passed in during initialization (similarly to ``Region``). This will require a bit of thought before implementing, and please talk to us about your ideas.

* Expiration times need to be added for all data types so that they can be cleared from the data sinks in the datapipeline when their data is no longer valid. This is serious undertaking and one we would like to work closely with you if you want to try this.
