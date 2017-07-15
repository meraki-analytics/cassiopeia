Type System: Cassiopeia's Class Structure
#########################################

Classes Hold Data
=================
The heart of the type system is the data that it holds.


Creating Objects
================
Objects that hold data from the Riot API can be created using two different interfaces. The ``cassiopeia.py`` file contains all methods to query for objects using method calls (e.g. ``cassiopeia.get_champions(region='NA')``). The second interface allows users to create objects directly using class constructors (e.g. ``annie = Champion(name='Annie', region='NA')``). See `here <>`_ for a list of methods, and `here <>`_ for the class constructors.

Ghost Objects
=============
Usually, when instantiated, a Cassiopeia object is a shell (or *ghost*) of an object and doesn't contain most of its data. For example, a ``Champion`` object may be instantiated via ``olaf = Champion(name="Olaf", id=1)`` which then only knows its ``id`` and ``name``. However, all Cass objects know how to load their own data. This allows Cass to have a more intuitive class structure and seamless user interface. Continuing the champion example, when ``olaf.title`` is accessed, the data won't exist, so the ``lol-static-data`` endpoint will be queried; similarly, if ``olaf.free_to_play`` is accessed, the ``status`` endpoint will be queried. Objects that access data from multiple endpoints (e.g. ``.title`` and ``.free_to_play`` for ``Champion``s) is one of the many benefits of Ghost objects.

