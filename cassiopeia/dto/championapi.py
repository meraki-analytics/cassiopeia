import cassiopeia.dto.requests
import cassiopeia.type.dto.champion


def get_champion_status(id_):
    """
    https://developer.riotgames.com/api/methods#!/1015/3443

    Args:
        id (int): the ID of the champion to look up

    Returns:
        Champion: the champion
    """
    request = "{version}/champion/{id_}".format(version=cassiopeia.dto.requests.api_versions["champion"], id_=id_)
    return cassiopeia.type.dto.champion.Champion(cassiopeia.dto.requests.get(request))


def get_champion_statuses(freeToPlay=False):
    """
    https://developer.riotgames.com/api/methods#!/1015/3444

    Args:
        freeToPlay (bool): whether to only get free to play champions (default False)

    Returns:
        list<Champion>: all the champions
    """
    request = "{version}/champion".format(version=cassiopeia.dto.requests.api_versions["champion"])
    return cassiopeia.type.dto.champion.ChampionList(cassiopeia.dto.requests.get(request, {"freeToPlay": freeToPlay}))
