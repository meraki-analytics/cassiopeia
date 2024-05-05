import cassiopeia as cass
from cassiopeia import FeaturedMatches, Summoner


def get_spectator_matches():
    featured_matches = cass.get_featured_matches(region="NA")
    for match in featured_matches:
        print(match.region, match.id)
    print()

    match = featured_matches[0]
    a_summoner = match.blue_team.participants[0].summoner
    a_summoner_name = a_summoner.account.name
    print(a_summoner_name)
    print(match.queue)

    summoner = Summoner(puuid=a_summoner.puuid, region=match.region)
    current_match = summoner.current_match
    print(current_match.map.name)

    print()
    for participant in current_match.blue_team.participants:
        print(participant.summoner.account.name)


if __name__ == "__main__":
    get_spectator_matches()
