""" Prints a selection of information about Dyrus' last match.  """

import os
import datetime
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    dyrus = riotapi.get_summoner_by_name("Dyrus")  # SummonerID is 5908

    match_list = riotapi.get_match_list(dyrus)
    match = riotapi.get_match(match_list[0])

    print("Basic match information:")
    print("  Match ID: {0}".format(match.id))
    print("  Version/Patch: {0}".format(match.version))
    print("  Creation date: {0}  (which was {1} ago)".format(match.creation, datetime.datetime.now() - match.creation))
    print("  Duration: {0}".format(match.duration))
    print("  Map: {0}".format(match.map))
    print("  Mode: {0}".format(match.mode))
    print("  Type: {0}".format(match.type))
    print("  Platform: {0}".format(match.platform))
    print("  Queue: {0}".format(match.queue))
    print("  Region: {0}".format(match.region))
    print("  Season: {0}".format(match.season))
    print("  Red Team Bans: {0}".format([ban.champion.name for ban in match.red_team.bans]))
    print("  Blue Team Bans: {0}".format([ban.champion.name for ban in match.blue_team.bans]))

    print()

    champion = match.participants["Dyrus"].champion

    print("You can use special key-words/key-objects to lookup the participants in the match.")
    print("  Lookup via Summoner:        {0}".format(match.participants[dyrus]))
    print("  Lookup via summoner name:   {0}".format(match.participants["Dyrus"]))
    print("  Lookup via Champion played: {0}".format(match.participants[champion]))
    print("  Lookup via champion name:   {0}".format(match.participants[champion.name]))

    print()

    # Print some basic information about the summoners in the game that doesn't require calls to the Summoner API.
    # If you ask for participant.summoner, Casseopeia will make a call to the Summoner API to get the full summoner information.
    print("Basic summoner information:")
    for participant in match.participants:
        print("  {0} ({1}) played {2}".format(participant.summoner_name, participant.summoner_id, participant.champion.name))

    print()

    # Print participant information (not summoner information)
    print("Participant information for this match:")
    for participant in match.participants:
        print("  {0}".format(participant.summoner_name))
        print("    Champion: {0}".format(participant.champion.name))
        print("    Won: {0}".format(participant.stats.win))
        print("    Side: {0}".format(participant.side))
        print("    Kills: {0}".format(participant.stats.kills))
        print("    Deaths: {0}".format(participant.stats.deaths))
        print("    Assists: {0}".format(participant.stats.assists))
        print("    KDA: {0}".format(participant.stats.kda))
        print("    CS: {0}".format(participant.stats.cs))
        print("    Summoner spells: {0} + {1}".format(participant.summoner_spell_d, participant.summoner_spell_f))
        print("    Champion Level: {0}".format(participant.stats.champion_level))
        print("    Got first blood: {0}".format(participant.stats.first_blood))
        print("    Gold earned: {0}".format(participant.stats.gold_earned))
        print("    Gold spent: {0}".format(participant.stats.gold_spent))
        print("    Items: {0}".format([item.name if item is not None else None for item in participant.stats.items]))
        print("    Magic Damage Dealt: {0}".format(participant.stats.magic_damage_dealt))
        print("    Physical Damage Dealt: {0}".format(participant.stats.physical_damage_dealt))
        print("    Lane: {0}".format(participant.timeline.lane))
        print("    Role: {0}".format(participant.timeline.role))

    print()

    print("Timestamp of last frame: {0}".format(match.frames[-1].timestamp))
    print("Number of events in last frame: {0}".format(len(match.frames[-1].events)))


if __name__ == "__main__":
    main()
