Pulling Data and Data Types
###########################

Pulling and interacting with data within ``cassiopeia.riotapi`` is designed to be simple and intuitive.

Let's work with a few short examples.

First, let's setup ``cassiopeia.riotapi``:

.. code-block:: python

  from cassiopeia import riotapi
  riotapi.set_region("NA")
  riotapi.set_api_key("Put-Your-API-Key-Here")

Now let's pull Dyrus' summoner information:

.. code-block:: python

    dyrus = riotapi.get_summoner_by_name("Dyrus")

That was easy. Is he in game right now?

.. code-block:: python

    game = riotapi.get_current_game(dyrus)
    if game is None:
        print("Dyrus is not in a game right now")
    else:
        print("Dyrus is in a game!")

or better yet we can get the ``game`` using

.. code-block:: python

    game = dyrus.current_game()

Notice how we use Dyrus' ``Summoner`` object to access his current game. You can use ``Summoner`` objects to pull many different types of data that require ``Summoner`` information, including ``Leagues``, ``Teams``, ``MatchList``, ``Stats``, ``ChampionMasteries``, etc.

If Dyrus is in game, what champion is he playing?

.. code-block:: python

    if game is not None:
        champion = game.participants["Dyrus"].champion
        print("Dyrus is playing {champion}".format(champion=champion.name))

Okay, you get the idea. Let's move on to a more in-depth example and look at one of Dyrus's recent matches.

.. code-block:: python

    match_list = dyrus.match_list()
    matchreference = match_list[-1]  # Get the last match reference in the list
    match = matchreference.match()

Now that we have the match, let's see what champions each participant played:

.. code-block:: python

    for participant in match.participants:
        print(participant.champion.name)

That was easy! Just a for loop and print. Now let's look at some of the events that happened in the match:

.. code-block:: python

    from cassiopeia.type.core.common import EventType
    for frame in match.timeline.frames:
        print("The following skill level up events occured between minute {} and {}".format(frame.timestamp.time.minute, frame.timestamp.time.minute + match.timeline.frame_interval))
        for event in frame:
            if event.type == EventType.skill_level_up:
                print("  {summoner} leveled up their {skill_slot}".format(summoner=event.creator.name, skill_slot=event.skill_slot))

We can also see how much gold every participant had at every minute:

.. code-block:: python

    for frame in match.timeline.frames:
        print("The amount of gold for each participant at minute {} was:".format(int(frame.timestamp.seconds/60)))
        for participant_frame in frame:
            print("  {summoner} had {amount} gold".format(summoner=participant_frame.participant.name, participant_frame.gold))

You can continue by pulling, accessing, and printing all of the information that the Riot API will return. By this point we hope you are beginning to understand the "flow" of Cassiopeia. Ideally, the code you write through Cassiopeia should be easily readable and understandable. That's our goal. Sometimes the lines get long, but this is normal for a service like the Riot API.

