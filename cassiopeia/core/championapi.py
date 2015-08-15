import cassiopeia.riotapi
import cassiopeia.dto.championapi
import cassiopeia.type.core.champion

# @param free_to_play # bool # Whether to only return free champions
# @return # dict<cassiopeia.type.core.staticdata.Champion, cassiopeia.type.core.champion.ChampionStatus> # The statuses for all champions
def get_champion_statuses(free_to_play=False):
    statuses = cassiopeia.dto.championapi.get_champion_statuses(free_to_play)
    
    # Always load champions since we'll be using them here
    cassiopeia.riotapi.get_champions()
    return {cassiopeia.riotapi.get_champion_by_id(champ.id): cassiopeia.type.core.champion.ChampionStatus(champ) for champ in statuses.champions}

# @param champion # cassiopeia.type.core.staticdata.Champion # The champion to get status for
# @return # cassiopeia.type.core.champion.ChampionStatus # The champion's status
def get_champion_status(champion):
    status = cassiopeia.dto.championapi.get_champion_status(champion.id)
    return cassiopeia.type.core.champion.ChampionStatus(status)