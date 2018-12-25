import cassiopeia as cass
from cassiopeia import Summoner


def print_newest_match(name: str,  region: str):
    summoner = Summoner(name=name, region=region)

    match_history = summoner.match_history
    match = match_history[0]
    print('Match ID:', match.id)

    print(match.timeline.frame_interval)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", region="NA")
