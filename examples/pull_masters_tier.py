"""
This example starts by getting the summoner information for every summoner in the
Masters tier. It then goes through those summoners, pulls their matchlist (getting
all matches after patch 5.14 started), and then goes through their matchlist and
pulls every game.

If you have an SQLAlchemy database set up, all of this information will be stored
automatically.

In addition, we define a helpful get_match function that automatically retries a
failed match request.
"""

import os
from datetime import datetime

from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.store import SQLAlchemyDB


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.eager)

    # Load and connect to your database. (Comment this code to use local memory. Don't forget to comment db.close() below too.)
    db = SQLAlchemyDB("mysql+mysqlconnector", "databse_hostname", "database_name", "username", "password")
    riotapi.set_data_store(db)

    master = [entry.summoner for entry in riotapi.get_master()]
    print("Pulled Master tier. Got {0} summoners.".format(len(master)))

    gather_start = datetime(2015, 7, 23)  # 1 day after patch 5.14
    for summoner in master:
        for match in summoner.match_list(begin_time=gather_start):
            # If you are connected to a database, the match will automatically be stored in it without you having to do anything.
            # Simply pull the match, and it's in your database for whenever you need it again!
            # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
            # and therefore will not count against your rate limit. This is true of all datatypes, not just Match.
            match = get_match(match)
            print("Stored {0} in my database".format(match))

    db.close()


def get_match(reference):
    """ Try to pull the referenced match from Riot's servers. If we can an error that
        we should retry, we will. If it fails a second time, we just skip it.
    """
    try:
        return riotapi.get_match(reference)
    except APIError as error:
        # Try Again Once
        if error.error_code in [500]:
            try:
                return riotapi.get_match(reference)
            except APIError as another_error:
                if another_error.error_code in [500, 400, 404]:
                    pass
                else:
                    raise another_error

        # Skip
        elif error.error_code in [400, 404]:
            pass

        # Fatal
        else:
            raise error


if __name__ == "__main__":
    main()
