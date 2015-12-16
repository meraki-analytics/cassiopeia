"""
This example pulls full match from the Riot API and looks through the participants
for role, lane, and side information. It stores these values in a dictionary and
prints them out.
"""

import os
from collections import namedtuple
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    # Pull the data for one of Dyrus' matches.
    match = riotapi.get_match(2034758953)

    # Create a namedtuple called "Info" that is used to store some information about participants.
    # We use a namedtuple because it allows for a clear way to access this data later in the script.
    Info = namedtuple("Info", ["side", "role", "lane"])

    # Loop through the participants in this match and record which side they played on (blue or red),
    # which role they played, and what lane they played in.
    mapping = {}
    for participant in match.participants:
        mapping[participant.champion.name] = Info(participant.side.name, participant.timeline.role.value, participant.timeline.lane.value)

    print()

    # Print out the information we just collected.
    for champion, info in sorted(mapping.items(), key=lambda tuple: (tuple[1].side, tuple[1].lane)):
        print("{0}: {1}".format(champion, info))


if __name__ == "__main__":
    main()
