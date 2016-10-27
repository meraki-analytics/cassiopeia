import cassiopeia.type.core.common
import cassiopeia.type.dto.common


@cassiopeia.type.core.common.inheritdocs
class Champion(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        active (bool): indicates if the champion is active
        botEnabled (bool): bot enabled flag (for custom games)
        botMmEnabled (bool): bot Match Made enabled flag (for Co-op vs. AI games)
        freeToPlay (bool): indicates if the champion is free to play. Free to play champions are rotated periodically
        id (int): champion ID. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        rankedPlayEnabled (bool): ranked play enabled flag
    """

    def __init__(self, dictionary):
        self.active = dictionary.get("active", False)
        self.botEnabled = dictionary.get("botEnabled", False)
        self.botMmEnabled = dictionary.get("botMmEnabled", False)
        self.freeToPlay = dictionary.get("freeToPlay", False)
        self.id = dictionary.get("id", 0)
        self.rankedPlayEnabled = dictionary.get("rankedPlayEnabled", False)


@cassiopeia.type.core.common.inheritdocs
class ChampionList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        champions (list<Champion>): the collection of champion information
    """

    def __init__(self, dictionary):
        self.champions = [(Champion(champ) if not isinstance(champ, Champion) else champ) for champ in
                          dictionary.get("champions", []) if champ]

    @property
    def champion_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for champ in self.champions:
            ids.add(champ.id)
        return ids
