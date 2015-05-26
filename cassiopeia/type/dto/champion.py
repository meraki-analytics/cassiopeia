from cassiopeia.type.dto.common import CassiopeiaDto

class Champion(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Indicates if the champion is active.
        self.active = dictionary["active"]

        # boolean # Bot enabled flag (for custom games).
        self.botEnabled = dictionary["botEnabled"]

        # boolean # Bot Match Made enabled flag (for Co-op vs. AI games).
        self.botMmEnabled = dictionary["botMmEnabled"]

        # boolean # Indicates if the champion is free to play. Free to play champions are rotated periodically.
        self.freeToPlay = dictionary["freeToPlay"]

        # long # Champion ID. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        self.id = dictionary["id"]

        # boolean # Ranked play enabled flag.
        self.rankedPlayEnabled = dictionary["rankedPlayEnabled"]


class ChampionList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Champion> # The collection of champion information.
        self.champions = [Champion(champ) if not isinstance(champ, Champion) else champ for champ in dictionary["champions"]]