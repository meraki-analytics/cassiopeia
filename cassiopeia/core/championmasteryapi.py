import cassiopeia.riotapi
import cassiopeia.core.requests
import cassiopeia.dto.championmasteryapi
import cassiopeia.type.core.championmastery
import cassiopeia.type.core.common


def get_champion_mastery(summoner, champion):
    """
    Gets the ChampionMastery object for the specified summoner and champion

    Args:
        summoner (Summoner): the summoner to get champion mastery for
        champion (Champion): the desired champion

    Returns:
        ChampionMastery: the summoner's champion mastery value for the specified champion
    """
    champion_mastery = cassiopeia.dto.championmasteryapi.get_champion_mastery(summoner.id, champion.id)
    return cassiopeia.type.core.championmastery.ChampionMastery(champion_mastery)


def get_champion_masteries(summoner):
    """
    Gets all the ChampionMastery objects for the specified summoner

    Args:
        summoner (Summoner): the summoner to get champion mastery for

    Returns:
        dict<Champion, ChampionMastery>: the summoner's champion masteries
    """
    champion_masteries = cassiopeia.dto.championmasteryapi.get_champion_masteries(summoner.id)

    # Always load champions since we'll be using them here
    cassiopeia.riotapi.get_champions()
    return {cassiopeia.riotapi.get_champion_by_id(cm.championId): cassiopeia.type.core.championmastery.ChampionMastery(cm) for cm in champion_masteries}


def get_champion_mastery_score(summoner):
    """
    Gets the total champion mastery score for the specified summoner

    Args:
        summoner (Summoner): the summoner to get champion mastery for

    Returns:
        int: the summoner's total champion mastery score
    """
    return cassiopeia.dto.championmasteryapi.get_champion_mastery_score(summoner.id)


def get_top_champion_masteries(summoner, max_entries=3):
    """
    Gets the top ChampionMastery objects for the specified summoner

    Args:
        summoner (Summoner): the summoner to get champion mastery for
        max_entries (int): the maximum number of entires to retrieve (default 3)

    Returns:
        list<ChampionMastery>: the summoner's top champion masteries
    """
    champion_masteries = cassiopeia.dto.championmasteryapi.get_top_champion_masteries(summoner.id, max_entries)

    # Load required data if loading policy is eager
    if champion_masteries and cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_champions()

    return [cassiopeia.type.core.championmastery.ChampionMastery(cm) for cm in champion_masteries]
