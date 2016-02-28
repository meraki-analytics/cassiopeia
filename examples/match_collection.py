"""
WARNING: Read this entire doc string before you run this program!

This example is an extension of pull_master_tier.py, so you should look at that first.
This is the "spiderweb" match collection idea that is often suggested on the Riot API
forums as the best way to collect a large number of matches.

It works as follows:

Given a match, we pull all the summoners in that match. Then for each of those summoners,
we collect their games via the matchlist endpoint, and then pull down all of their matches
and save them to a database. In Cassiopeia, if you have set up your SQLAlchemy databse then
every match (and in fact every summoner, etc.) gets stored in your database automatically.
This makes it reasonably easy to pull matches and create a large databse.

The algorithm will simply keep doing this until you, the user, stop it. Make sure you keep an
eye on how large your database is getting! You may want to put a conditional break statement
somewhere in the code.

In order for the algorithm to start, we need a match or a summoner to start the lookup. We
first pull the Master tier and use those summoners as seed data. For the rest of the match
collection.
"""

import os
from datetime import datetime
from collections import deque

from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.store import SQLAlchemyDB


def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable) and skip 400s (Bad Request) or 404s (Not Found). """
    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
            # Try Again Once
            if error.error_code in [500]:
                try:
                    print("Got a 500, trying again...")
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 400, 404]:
                        pass
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                print("Got a 400 or 404")
                pass

            # Fatal
            else:
                raise error
    return call_wrapper


# Set get_match and get_summoner_by* to automatically retry if we get a 500, or skip if we get a 400 or 403
# The above decorator wraps these functions, applying the functionality in the decorator to the wrapped functions.
riotapi.get_match = auto_retry(riotapi.get_match)
riotapi.get_summoner_by_id = auto_retry(riotapi.get_summoner_by_id)
riotapi.get_summoner_by_name = auto_retry(riotapi.get_summoner_by_name)


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    # Load and connect to your database. (Comment this code to use local memory. Don't forget to comment db.close() below too.)
    db = SQLAlchemyDB("mysql+mysqlconnector", "databse_hostname", "database_name", "username", "password")
    riotapi.set_data_store(db)

    # We will seed with all the summoners in Master's tier
    unpulled_summoners = deque(entry.summoner for entry in riotapi.get_master())
    print("Pulled Master tier for seeding. Got {0} summoners.".format(len(unpulled_summoners)))

    # We need this so that we don't get a recursive loop of summoners
    pulled_summoners = deque()

    gather_start = datetime(2015, 7, 23)  # 1 day after patch 5.14

    while len(unpulled_summoners) > 0:
        summoner = unpulled_summoners.popleft()
        for match_reference in summoner.match_list(begin_time=gather_start):
            # If you are connected to a database, the match will automatically be stored in it without you having to do anything.
            # Simply pull the match, and it's in your database for whenever you need it again!
            # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
            # and therefore will not count against your rate limit. This is true of all datatypes, include Summoner.
            match = riotapi.get_match(match_reference)
            print("Stored {0} in my database".format(match))
            for participant in match.participants:
                if participant.summoner not in unpulled_summoners and participant.summoner not in pulled_summoners:
                    unpulled_summoners.append(participant.summoner)
        pulled_summoners.append(summoner)

    db.close()

if __name__ == "__main__":
    main()
