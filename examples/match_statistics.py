import cassiopeia as cass
from cassiopeia import Summoner

cass.set_riot_api_key("API_KEY")


def get_participant_data(participants):
    team_participant_data = []
    for p in participants:
        p_data = {"summoner": p.summoner.name, "champion": p.champion.name, "runes": p.runes.keystone.name,
                    "d_spell": p.summoner_spell_d.name, "f_spell": p.summoner_spell_f.name,
                    "kills": p.stats.kills, "assist": p.stats.assists, "deaths": p.stats.deaths,
                    "kda_ratio": round(p.stats.kda, 2), "damage_dealt": p.stats.total_damage_dealt,
                    "creep_score": p.stats.total_minions_killed, "vision_score": p.stats.vision_score}

        p_items = []
        number_of_item_slots = 6
        for i in range(number_of_item_slots):
            try:
                p_items.append(p.stats.items[i].name)
            except AttributeError:
                p_items.append("None")
        p_data["items"] = p_items
        team_participant_data.append(p_data)
    return team_participant_data


def print_match_history(summoner, num_matches):
    for i, match in enumerate(summoner.match_history[0:num_matches], start=1):
        match_num = f"MATCH {i}"
        print(match_num.center(100, "#"))

        blue_team = match.blue_team.participants
        print("BLUE SIDE".center(100, "-"))
        for p_data in get_participant_data(blue_team):
            print(p_data)

        red_team = match.red_team.participants
        print("RED SIDE".center(100, "-"))
        for p_data in get_participant_data(red_team):
            print(p_data)


def main():
    name = "Irucin"
    server = "NA"
    summoner = Summoner(name=name, region=server)
    print_match_history(summoner, 5)


if __name__ == "__main__":
    main()
