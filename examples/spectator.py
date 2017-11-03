import cassiopeia as cass
from cassiopeia import Summoner, FeaturedMatches


def get_spectator_matches():
    featured_matches = cass.get_featured_matches(region="NA")
    for match in featured_matches:
        print(match.region, match.id)

    match = featured_matches[0]
    a_summoner_name = match.blue_team.participants[0].summoner.name
    print(match.queue)
    summoner = Summoner(name=a_summoner_name, region=match.region)
    current_match = summoner.current_match
    print(current_match.map.name)

    for participant in current_match.blue_team.participants:
        print(participant.summoner.name)


if __name__ == "__main__":
    get_spectator_matches()
