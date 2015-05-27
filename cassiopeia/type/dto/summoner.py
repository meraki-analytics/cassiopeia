from cassiopeia.type.dto.common import CassiopeiaDto

class RunePages(CassiopeiaDto):
    def __init__(self, dictionary):
        # set<RunePage> # Collection of rune pages associated with the summoner.
        self.pages = set(RunePage(p) if not isinstance(p,RunePage) else p for p in dictionary.get("pages",[]))

        # long # Summoner ID.
        self.summonerId = dictionary.get("summonerId",0)


class RunePage(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Indicates if the page is the current page.
        self.current = dictionary.get("current",False)

        # long # Rune page ID.
        self.id = dictionary.get("id",0)

        # string # Rune page name.
        self.name = dictionary.get("name",'')

        # set<RuneSlot> # Collection of rune slots associated with the rune page.
        self.slots = set(RuneSlot(s) if not isinstance(s,RuneSlot) else s for s in dictionary.get("slots",[]))


class RuneSlot(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API.
        self.runeId = dictionary.get("runeId",0)

        # int # Rune slot ID.
        self.runeSlotId = dictionary.get("runeSlotId",0)


class MasteryPages(CassiopeiaDto):
    def __init__(self, dictionary):
        # set<MasteryPage> # Collection of mastery pages associated with the summoner.
        self.pages = set(MasteryPage(p) if not isinstance(p,MasteryPage) else p for p in dictionary.get("pages",[]))

        # long # Summoner ID.
        self.summonerId = dictionary.get("summonerId",0)


class MasteryPage(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Indicates if the mastery page is the current mastery page.
        self.current = dictionary.get("current",False)

        # long # Mastery page ID.
        self.id = dictionary.get("id",0)

        # list<MasteryDto> # Collection of masteries associated with the mastery page.
        self.masteries = dictionary.get("masteries",[])

        # string # Mastery page name.
        self.name = dictionary.get("name",'')


class Mastery(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Mastery ID. For static information correlating to masteries, please refer to the LoL Static Data API.
        self.id = dictionary.get("id",0)

        # int # Mastery rank (i.e., the number of points put into this mastery).
        self.rank = dictionary.get("rank",0)


class Summoner(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Summoner ID.
        self.id = dictionary.get("id",0)

        # string # Summoner name.
        self.name = dictionary.get("name",'')

        # int # ID of the summoner icon associated with the summoner.
        self.profileIconId = dictionary.get("profileIconId",0)

        # long # Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change
        self.revisionDate = dictionary.get("revisionDate",0)

        # long # Summoner level associated with the summoner.
        self.summonerLevel = dictionary.get("summonerLevel",0)