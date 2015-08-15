import sqlalchemy

import cassiopeia.type.dto.common

class Champion(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "ChampionStatus"
    active = sqlalchemy.Column(sqlalchemy.Boolean)
    botEnabled = sqlalchemy.Column(sqlalchemy.Boolean)
    botMmEnabled = sqlalchemy.Column(sqlalchemy.Boolean)
    freeToPlay = sqlalchemy.Column(sqlalchemy.Boolean)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    rankedPlayEnabled = sqlalchemy.Column(sqlalchemy.Boolean)

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


class ChampionList(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Champion> # The collection of champion information.
        self.champions = [(Champion(champ) if not isinstance(champ, Champion) else champ) for champ in dictionary.get("champions", []) if champ]

    @property
    def champion_ids(self):
        ids = set()
        for champ in self.champions:
            ids.add(champ.id)
        return ids
