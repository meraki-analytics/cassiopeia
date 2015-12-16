"""
This examples shows some nice functionality when looking at data/time elements
such as the match create date+time and the match duration. Using these two
Cassiopeia values, we can simply add them together and get the date+time when
the match ended.

In addition, we print the match version.
"""

import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    match = riotapi.get_match(2034758953)

    print("Match start time: {0}".format(match.creation))
    print("Match duration: {0}".format(match.duration))

    # You can just add them together!
    print("Match end time: {0}".format(match.creation + match.duration))

    print("Match version: {0}".format(match.version))


if __name__ == "__main__":
    main()
