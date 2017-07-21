import cassiopeia as cass
from cassiopeia.core import CurrentMatch, Summoner


def get_spectator_matches():
    featured_matches = cass.get_featured_matches("NA")
    for match in featured_matches:
        print(match.id)

    match = featured_matches[0]
    a_summoner_name = match.blue_team.participants[0].summoner_name
    summoner = Summoner(name=a_summoner_name, region=match.region)
    # TODO This doesn't work because the summoner_id needs to be passed in in a special way, analogous to match.
    # This will take some work to fix, and I'm skipping it for now.
    current_match = CurrentMatch(id=featured_matches[0].id, region=featured_matches[0].region, summoner_id=summoner.id)
    print(current_match.map)



if __name__ == "__main__":
    get_spectator_matches()
