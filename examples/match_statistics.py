import cassiopeia as cass
from cassiopeia import Summoner

cass.set_riot_api_key("API_KEY")


class MatchStatistics:
    def __init__(self, ign, region):
        self.ign = ign
        self.region = region

    def match_history(self):
        b = "BLUE SIDE"
        r = "RED SIDE"
        summoner = Summoner(name=self.ign, region=self.region)

        for i in range(5):
            match_num = "MATCH " + str(i+1)
            print(match_num.center(100, '#'))

            match = summoner.match_history[i]
            participants = match.participants
            blue_side = match.blue_team.participants
            red_side = match.red_team.participants

            self.print_lobby(b, blue_side)
            self.print_lobby(r, red_side)

    @staticmethod
    def get_side(side):
        lobby = []
        for p in side:
            p_row = {'summoner': p.summoner.name, 'champion': p.champion.name, 'runes': p.runes.keystone.name,
                     'd_spell': p.summoner_spell_d.name, 'f_spell': p.summoner_spell_f.name,
                     'kills': p.stats.kills, 'assist': p.stats.assists, 'deaths': p.stats.deaths,
                     'kda_ratio': round(p.stats.kda, 2), 'damage_dealt': p.stats.total_damage_dealt,
                     'creep_score': p.stats.total_minions_killed, 'vision_score': p.stats.vision_score}

            temp = []
            for i in range(6):
                try:
                    temp.append(p.stats.items[i].name)
                except AttributeError:
                    temp.append("None")
            p_row['items'] = temp
            lobby.append(p_row)
        return lobby

    @staticmethod
    def print_lobby(side, lobby):
        print(side.center(100, '-'))
        for team in MatchStatistics.get_side(lobby):
            print(team)


def main():
    name = "Irucin"
    server = "NA"
    match_stats = MatchStatistics(name, server)
    match_stats.match_history()


main()
