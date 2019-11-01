import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue
from collections import Counter


def print_newest_match(name: str, region: str):

    # Notice how this function never makes a call to the summoner endpoint because we provide all the needed data!

    summoner = Summoner(name=name, region=region)

    # A MatchHistory is a lazy list, meaning it's elements only get loaded as-needed.

    # match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_8}, queues={Queue.ranked_solo_fives})
    match_history = summoner.match_history
    match_history(seasons={Season.season_9}, queues={Queue.ranked_solo_fives})

    # Load the entire match history by iterating over all its elements so that we know how long it is.
    # Unfortunately since we are iterating over the match history and accessing the summoner's champion for each match,
    # we need to know what version of the static data the champion should have. To avoid pulling many different
    # static data versions, we will instead create a {champion_id -> champion_name} mapping and just access the champion's
    # ID from the match data (which it provides directly).
    champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region=region)}
    played_champions = Counter()
    for match in match_history:
        champion_id = match.participants[summoner.name].champion.id
        champion_name = champion_id_to_name_mapping[champion_id]
        played_champions[champion_name] += 1
    print("Length of match history:", len(match_history))

    # Print the aggregated champion results
    print("Top 10 champions {} played:".format(summoner.name))
    for champion_name, count in played_champions.most_common(10):
        print(champion_name, count)
    print()

    match = match_history[0]
    print('Match ID:', match.id)

    p = match.participants[summoner]
    print("\nSince the match was created from a matchref, we only know one participant:")
    #print(p.summoner.name, 'playing', p.champion.name)
    print(p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id)

    print("\nNow pull the full match data by iterating over all the participants:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon, p.runes.keystone.name)

    print("\nIterate over all the participants again and note that the data is not repulled:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon, p.runes.keystone.name)

    print("\nBlue team won?", match.blue_team.win)
    print("Red team won?", match.red_team.win)
    print("Participants on blue team:")
    for p in match.blue_team.participants:
        print(p.summoner.name, p.champion.name)

    # Print keystone and the stat runes for each player/champion
    for p in match.participants:
        print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.stat_runes])


if __name__ == "__main__":
    print_newest_match(name="Kalturi", region="NA")
