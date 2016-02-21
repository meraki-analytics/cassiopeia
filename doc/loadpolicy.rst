Load Policies and Lazy Loading
##############################

Understanding Cassiopeia's load policy is key to using the library to its full potential.

Note that the load policy only matters when using ``riotapi``. ``baseriotapi`` does not use the advanced loading polices or lazy loading.

Object-Level Lazy Loading
=========================

Many of the API objects that the ``riotapi`` produces use Object-Level Lazy Loading to acheive the Cassiopeia's usability goals. It is very rare to use all the information available from an API call, and usually you are only looking for a few specific pieces of data. Object-Level Lazy Loading ensures that time and memory are not wasted on data you are not using. 

Cassiopeia will delay the loading of some objects' attributes if those attributes require a noteable amount of time to load. For example, when you pull a match using the ``get_match`` `method <cassiopeia/riotapi.html#cassiopeia.riotapi.get_match>`_, Cassiopeia does not immediately load the match's ``timeline`` because this is a very large subset of information that you may never use. Instead, the first time you try to access ``match.timeline`` this data is loaded, and if you never access ``match.timeline`` then the data is never rendered and compution time is saved.

Load Policies
=============

There are two types of load policies in Cassiopeia, Eager and Lazy, which determine how calls to the Riot API are handled.

You should think of Eager loading as a useful extension of the usual way a library would handle API requests, and Lazy loading as the "standard" way. Note that the Lazy load policy is distinct from the Object-Level Lazy Loading described above (which is always done regardless of load policy).

Normally, when you want to access information from Riot, you send them an API request. However, if you know in advance that you will need data for a bunch of different objects, you can group those calls together. For example, Riot's Summoner endpoint allows 40 summoners to be queried at once so you shouldn't make 40 different calls to get data for 40 summoners, you should only make one. Cassiopeia will automatically group these calls together when using its Eager loading policy.

Lazy
^^^^

The Lazy loading policy will only pull additional data from Riot when you attempt to access it for the first time. This is the "standard" way of making API requests.

The Lazy loading policy can be set with ``riotapi.set_load_policy("lazy")`` and should be used when you only want the requested data and will not use other information that needs to be requested from Riot.

Eager
^^^^^

When using the Eager loading policy, Cassiopeia may perform more calls than the one you wrote. Cassiopeia will pull all data that is referenced within any objects that were pulled from Riot.

The Eager loading policy can be set with ``riotapi.set_load_policy("eager")`` and should be used when you need additional information about the objects that require additional API calls.

Example
=======

Consider the following example to determine when to use Eager loading and when to use Lazy loading.

We will pull all summoners from the Challenger league and either print their names, or print their names and the date of their most recent game.

Lazy
^^^^

Use Lazy loading when you only need to access data that is returned directly from the call you made (for this example see `Riot's documentation <https://developer.riotgames.com/api/methods#!/985/3353>`_ and `Cassiopeia's documentation <cassiopeia/type/core/index.html#cassiopeia.type.core.league.Entry>`_).

.. code-block:: python

    riotapi.set_load_policy("lazy")
    riotapi.print_calls(True)
    challenger = riotapi.get_challenger()

    for entry in challenger:
        name = entry.summoner_name
        print("  {name}".format(name=name))

Eager
^^^^^

However, when you want to access additional information about an object that was not returned from Riot (in this case the each summoner's last modification date) you should use Eager loading.

The Riot API allows users to pull data for up to 40 summoners with one call. When ``get_challenger`` is called, Cassiopeia sees that ``Summoner`` objects are referenced within each ``Entry`` in the return value. After Cassiopeia has finished with the ``get_challenger`` request, it will then perform one or more additional API calls to ``get_summoners_by_id`` and pass in a list of summoner ids that were returned from ``get_challenger``.

.. code-block:: python

    riotapi.set_load_policy("eager")
    riotapi.print_calls(True)
    challenger = riotapi.get_challenger()

    for entry in challenger:
        name = entry.summoner_name
        date = entry.summoner.modify_date
        print("{name} last played a game on {data}".format(name=name, date=date))

If you run this code with the Lazy loading policy, when the line ``date = entry.summoner.modify_date`` is run, Cassiopeia will try to access ``entry.summoner`` but that object will not exist. Cassiopeia will then make a ``get_summoner_by_id`` (note ``summoner`` and not ``summoners``) call to Riot within the ``for`` loop. This will require up to 40x more requests to Riot (which takes far longer and uses up requests in your rate limiter) than the Eager loading case because each summoner is pulled individually.
