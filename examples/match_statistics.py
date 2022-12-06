import cassiopeia as cass
from cassiopeia import Summoner, Match, Rank, Queue

ign = "Irucin"
region = "NA"

summoner = Summoner(name=ign, region=region)
match = summoner.match_history[0]
participants = match.participants

blue = match.blue_team.participants
red = match.red_team.participants

print("--------------*BLUE*--------------")
for p in blue:
    L = []
    for i in range(6):
        try:
            L.append(p.stats.items[i].name)
        except AttributeError:
            L.append("None")

    print(p.summoner.name + " - " +
          p.champion.name + " - " +
          p.runes.keystone.name + " - " +
          p.summoner_spell_d.name + "/" +
          p.summoner_spell_f.name + " - " + str(p.summoner.ranks[Queue("RANKED_SOLO_5x5")]) + " - KDA: " +
          str(p.stats.kills) + "/" + str(p.stats.assists) + "/" + str(p.stats.deaths) + "=" + str(p.stats.kda) +
          " - Damage Dealt: " +
          str(p.stats.total_damage_dealt) + " - CS: " +
          str(p.stats.total_minions_killed) + " - Vision Score: " +
          str(p.stats.vision_score)
          )
    print("Items: ", L[0], L[1], L[2], L[3], L[4], L[5])

    # for i in range(6):
    #     try:
    #         print(p.stats.items[i].name)
    #     except AttributeError:
    #         print("Empty")

# print("--------------*RED*--------------")
# for p in red:
#     print(p.summoner.name)
# print(match)
