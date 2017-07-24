import cassiopeia as cass
from cassiopeia.core import Summoner, Champion, ChampionMastery

def print_champion_mastery():
    # Name: Kalturi
    # ID: 21359666
    # Account ID: 34718348

    me = Summoner(name="Kalturi", id=21359666)
    karma = Champion(name="Karma", id=43)
    #cm = ChampionMastery(champion=karma, summoner=me)
    cm = cass.get_champion_mastery(champion=karma, summoner=me)
    print('Champion ID:', cm.champion.id)
    print('Mastery points:', cm.points)
    print('Mastery Level:', cm.level)
    print('Points until next level:', cm.points_until_next_level)

    cms = cass.get_champion_masteries(summoner=me)
    cms = me.champion_masteries
    print(cms[0].points)
    # print(cms["Karma"].points)  # Does a ton of calls without a cache

    print("{} has mastery level 6 or higher on:".format(me.name))
    pro = cms.filter(lambda cm: cm.level >= 6)
    print([cm.champion.name for cm in pro])


if __name__ == "__main__":
    print_champion_mastery()
