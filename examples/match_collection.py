import random
from sortedcontainers import SortedList
import datetime

from cassiopeia.core import Summoner, MatchHistory, Match
from cassiopeia.data import Queue, Patch


def filter_match_history(summoner, patch):
    end_time = patch.end
    if end_time is None:
        end_time = datetime.datetime.now()
    match_history = MatchHistory(summoner=summoner, region=summoner.region, queues={Queue.aram}, begin_time=patch.start, end_time=end_time)
    return match_history


def collect_matches():
    initial_summoner_name = "GustavEnk"
    region = "EUW"

    summoner = Summoner(name=initial_summoner_name, region=region)
    patch_720 = Patch.from_str("7.20")

    unpulled_summoner_ids = SortedList([summoner.id])
    pulled_summoner_ids = SortedList()

    unpulled_match_ids = SortedList()
    pulled_match_ids = SortedList()

    while unpulled_summoner_ids:
        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        matches = filter_match_history(new_summoner, patch_720)
        unpulled_match_ids.update([match.id for match in matches])
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)

        while unpulled_match_ids:
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            new_match = Match(id=new_match_id, region=region)
            for participant in new_match.participants:
                if participant.summoner.id not in pulled_summoner_ids and participant.summoner.id not in unpulled_summoner_ids:
                    unpulled_summoner_ids.add(participant.summoner.id)
            # The above lines will trigger the match to load its data by iterating over all the participants.
            # If you have a database in your datapipeline, the match will automatically be stored in it.
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)


if __name__ == "__main__":
    collect_matches()
