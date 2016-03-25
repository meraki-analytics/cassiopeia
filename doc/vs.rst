Riot API vs. Base Riot API
##########################

This section explains the differences between ``cassiopeia.riotapi`` and ``cassiopeia.baseriotapi``.

We highly recommend using ``riotapi`` because it provides a suite of tools and usability improvements that make using the Riot API easy and fun.

Riot API
========

* Usage: ``from cassiopeia import riotapi``
* Automatically throttles requests to fit `rate limits <ratelimiting.html>`_
* Useability-focused type system that replaces foreign key ID values with the referenced object to make using the Riot API easy

  * e.g. ``match.participants['Dyrus'].champion`` returns a ``Champion`` object so you can easily access information such as the champion name or image url: ``match.participants['Dyrus'].champion.name`` or ``match.participants['Dyrus'].champion.image.link``

* Option to `lazy load <loadpolicy.html#lazy>`_ referenced objects right when you need them or batch them up and `eagerly load <loadpolicy.html#eager>`_ them to minimize API calls
* Caches static data and summoner information to accelerate access and reduce API load
* Available automatic databasing using `SQLAlchemy <http://www.sqlalchemy.org/>`_


Base Riot API
=============

* Usage: ``from cassiopeia import baseriotapi``
* Automatically throttles requests to fit `rate limits <ratelimiting.html>`_
* Meets the Riot API specification exactly and foreign keys are not auto-filled

  * e.g. ``match.participants[3].championId``

* Make only the requests you want to make
