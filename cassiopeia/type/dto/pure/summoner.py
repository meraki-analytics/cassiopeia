from cassiopeia.type.dto.pure.common import CassiopeiaDto
import cassiopeia.type.core.common


@cassiopeia.type.core.common.inheritdocs
class RunePages(CassiopeiaDto):
    """
    pages         list<RunePage>    collection of rune pages associated with the summoner
    summonerId    int               summoner ID
    """
    def __init__(self, dictionary):
        self.pages = [(RunePage(p) if not isinstance(p, RunePage) else p) for p in dictionary.get("pages", []) if p]
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def rune_ids(self):
        """Gets all rune IDs contained in this object"""
        ids = set()
        for p in self.pages:
            ids = ids | p.rune_ids
        return ids


@cassiopeia.type.core.common.inheritdocs
class RunePage(CassiopeiaDto):
    """
    current    bool              indicates if the page is the current page
    id         int               rune page ID
    name       str               rune page name
    slots      list<RuneSlot>    collection of rune slots associated with the rune page
    """
    def __init__(self, dictionary):
        self.current = dictionary.get("current", False)
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.slots = [(RuneSlot(s) if not isinstance(s, RuneSlot) else s) for s in dictionary.get("slots", []) if s]

    @property
    def rune_ids(self):
        """Gets all rune IDs contained in this object"""
        ids = set()
        for s in self.slots:
            if(s.runeId):
                ids.add(s.runeId)
        return ids


@cassiopeia.type.core.common.inheritdocs
class RuneSlot(CassiopeiaDto):
    """
    runeId        int    rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API.
    runeSlotId    int    rune slot ID.
    """
    def __init__(self, dictionary):
        self.runeId = dictionary.get("runeId", 0)
        self.runeSlotId = dictionary.get("runeSlotId", 0)


@cassiopeia.type.core.common.inheritdocs
class MasteryPages(CassiopeiaDto):
    """
    pages         list<MasteryPage>    collection of mastery pages associated with the summoner
    summonerId    int                  summoner ID
    """
    def __init__(self, dictionary):
        self.pages = [(MasteryPage(p) if not isinstance(p, MasteryPage) else p) for p in dictionary.get("pages", []) if p]
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def mastery_ids(self):
        """Gets all mastery IDs contained in this object"""
        ids = set()
        for p in self.pages:
            ids = ids | p.mastery_ids
        return ids


@cassiopeia.type.core.common.inheritdocs
class MasteryPage(CassiopeiaDto):
    """
    current      bool                indicates if the mastery page is the current mastery page
    id           int                 mastery page ID
    masteries    list<MasteryDto>    collection of masteries associated with the mastery page
    name         str                 mastery page name.
    """
    def __init__(self, dictionary):
        self.current = dictionary.get("current", False)
        self.id = dictionary.get("id", 0)
        self.masteries = [(Mastery(s) if not isinstance(s, Mastery) else s) for s in dictionary.get("masteries", []) if s]
        self.name = dictionary.get("name", "")

    @property
    def mastery_ids(self):
        """Gets all mastery IDs contained in this object"""
        ids = set()
        for m in self.masteries:
            if(m.id):
                ids.add(m.id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class Mastery(CassiopeiaDto):
    """
    id      int    mastery ID. For static information correlating to masteries, please refer to the LoL Static Data API.
    rank    int    mastery rank (i.e. the number of points put into this mastery)
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.rank = dictionary.get("rank", 0)


@cassiopeia.type.core.common.inheritdocs
class Summoner(CassiopeiaDto):
    """
    id               int    summoner ID
    name             str    summoner name
    profileIconId    int    ID of the summoner icon associated with the summoner
    revisionDate     int    date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change.
    summonerLevel    int    summoner level associated with the summoner
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.profileIconId = dictionary.get("profileIconId", 0)
        self.revisionDate = dictionary.get("revisionDate", 0)
        self.summonerLevel = dictionary.get("summonerLevel", 0)