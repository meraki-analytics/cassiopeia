import cassiopeia as cass
from cassiopeia.core import Summoner, Champion, ChampionMastery

def test_cass():
    # Name: Kalturi
    # Id: 21359666
    # Account id: 34718348

    me = Summoner(name="Kalturi", id=21359666)
    karma = Champion(name="Karma")
    cm = ChampionMastery(champion=karma, summoner=me)
    cm = cass.get_champion_mastery(champion=karma, summoner=me)
    print(cm.champion.id)
    print(cm.points)
    print(cm.level)
    print(cm.points_until_next_level)
    print(cm.champion.id)
    print()

    #cms = cass.get_champion_masteries(summoner=me)
    cms = me.champion_masteries
    print(cms[0].points)
    #print(cms["Karma"].points)  # Does a ton of calls without a cache
    return


if __name__ == "__main__":
    test_cass()
