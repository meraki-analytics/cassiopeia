import cassiopeia.riotapi
import cassiopeia.dto.championapi
import cassiopeia.type.core.champion


def get_champion_statuses(free_to_play=False):
    """
    Gets the statuses for all champions (whether they are disabled, etc.)

    Args:
        free_to_play (bool): whether to only return free champions (default False)

    Returns:
        dict<Champion, ChampionStatus>: the statuses for all the champions
    """
    statuses = cassiopeia.dto.championapi.get_champion_statuses(free_to_play)

    # Always load champions since we'll be using them here
    cassiopeia.riotapi.get_champions()
    return {cassiopeia.riotapi.get_champion_by_id(champ.id): cassiopeia.type.core.champion.ChampionStatus(champ) for champ in statuses.champions}


def get_champion_status(champion):
    """
    Gets the status for a champion (whether they are disabled, etc.)

    Args:
        champion (Champion): the champion to get the status of

    Returns:
        ChampionStatus: the champion's status
    """
    status = cassiopeia.dto.championapi.get_champion_status(champion.id)
    return cassiopeia.type.core.champion.ChampionStatus(status)
