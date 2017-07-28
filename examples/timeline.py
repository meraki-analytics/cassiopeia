import cassiopeia as cass
from cassiopeia.core import Summoner


def print_newest_match(name: str, account: int, id: int, region: str):
    summoner = Summoner(name=name, account=account, id=id, region=region)

    match_history = summoner.match_history
    match = match_history[0]
    print('Match ID:', match.id)

    print(match.timeline.frame_interval)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", account=34718348, id=21359666, region="NA")
