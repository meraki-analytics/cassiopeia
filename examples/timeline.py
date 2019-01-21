import datetime
import cassiopeia as cass
from cassiopeia import Summoner


def print_newest_match(name: str,  region: str):
    summoner = Summoner(name=name, region=region)

    match_history = summoner.match_history(queues={cass.Queue.ranked_solo_fives})
    match = match_history[0]
    print("Match ID:", match.id)

    print("Frame interval:", match.timeline.frame_interval)

    # The cumulative timeline property allows you to get some info about participants during the match.
    #  You access the cumulative timeline by providing the duration into the game that you want the info for.
    #  In this case, we're accessing the game at 15 minutes and 30 seconds.
    #  Some data is only available every one minute.
    p = match.participants[summoner]
    p_state = p.cumulative_timeline[datetime.timedelta(minutes=15, seconds=30)]
    # You can also use a string instead of datetime.timedelta
    p_state = p.cumulative_timeline["15:30"]
    items = p_state.items
    items = [item.name for item in items]
    skills = p_state.skills
    print("Champion:", p.champion.name)
    print("Items:", items)
    print("Skills:", skills)
    print("Kills:", p_state.kills)
    print("Deaths:", p_state.deaths)
    print("Assists:", p_state.assists)
    print("KDA:", p_state.kda)
    print("Level:", p_state.level)
    print("Position:", p_state.position)
    print("Exp:", p_state.experience)
    print("Number of objectives assisted in:", p_state.objectives)
    print("Gold earned:", p_state.gold_earned)
    print("Current gold:", p_state.current_gold)
    print("CS:", p_state.creep_score)
    print("CS in jungle:", p_state.neutral_minions_killed)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", region="NA")
