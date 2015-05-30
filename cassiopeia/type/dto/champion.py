from cassiopeia.type.dto.common import CassiopeiaDto

class Champion(CassiopeiaDto):
    def __init__(self, dictionary):
        # bool # Indicates if the champion is active.
        self.active = dictionary.get("active", False)

        # bool # Bot enabled flag (for custom games).
        self.botEnabled = dictionary.get("botEnabled", False)

        # bool # Bot Match Made enabled flag (for Co-op vs. AI games).
        self.botMmEnabled = dictionary.get("botMmEnabled", False)

        # bool # Indicates if the champion is free to play. Free to play champions are rotated periodically.
        self.freeToPlay = dictionary.get("freeToPlay", False)

        # int # Champion ID. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        self.id = dictionary.get("id", 0)

        # bool # Ranked play enabled flag.
        self.rankedPlayEnabled = dictionary.get("rankedPlayEnabled", False)


class ChampionList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Champion> # The collection of champion information.
        self.champions = [(Champion(champ) if not isinstance(champ, Champion) else champ) for champ in dictionary.get("champions", []) if champ]