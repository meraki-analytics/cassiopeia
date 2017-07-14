Cassiopeia Documentation
########################

What is Cassiopeia?
===================

Cassiopeia (which we fondly call Cass) is a framework for pulling and working with data from the `Riot API <https://developer.riotgames.com/>`_. Cass differentiates itself from other API wrappers by taking a page from one of Cassiopeia's quotes, "I'll take care of everything." Our main goal is to make your life (and ours) as a developer *easy*.

Cass is composed of three key pieces: 1) An interface for pulling data from the Riot API. 2) A "type system" of classes that holds the data pulled from Riot. 3) A way to temporarily and permanently store that data. These three pieces are tightly and seemlessly integrated, and as a user it may not be immediately apparent how that happens. Luckily, as a user, you can simply use Cass and get its features without needing to know the details.

Contributions are welcome! If you have idea or opinions on how things can be improved, don't hesitate to let us know by posting an issue on GitHub or @ing us on the Discord channel. And we always want to hear from our users, even (especially) if it's just letting us know what you are using Cass for.


Overview
========

.. toctree::
    :maxdepth: 1

    setup


Top Level APIs
==============

.. toctree::
    :maxdepth: 1

    cassiopeia/cassiopeia


Submodules used by APIs
=======================

Type System
^^^^^^^^^^^

.. toctree::
    :maxdepth: 1

    cassiopeia/core/index
    cassiopeia/dto/index


Index and Search
################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`