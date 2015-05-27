from cassiopeia.type.dto.common import CassiopeiaDto

class RunePages(CassiopeiaDto):
    def __init__(self, dictionary):
        # Set<RunePage> # Collection of rune pages associated with the summoner.
        self.pages = {RunePage(p) if not isinstance(p,RunePage) else p for p in dictionary["pages"]}

        # long # Summoner ID.
        self.summonerId = dictionary["summonerId"]


class RunePage(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Indicates if the page is the current page.
        self.current = dictionary["current"]

        # long # Rune page ID.
        self.id = dictionary["id"]

        # string # Rune page name.
        self.name = dictionary["name"]

        # Set<RuneSlot> # Collection of rune slots associated with the rune page.
        self.slots = {RuneSlot(s) if not isinstance(s,RuneSlot) else s for s in dictionary["slots"]}


class RuneSlot(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API.
        self.runeId = dictionary["runeId"]

        # int # Rune slot ID.
        self.runeSlotId = dictionary["runeSlotId"]


class MasteryPages(CassiopeiaDto):
    def __init__(self, dictionary):
        # Set<MasteryPage> # Collection of mastery pages associated with the summoner.
        self.pages = {MasteryPage(p) if not isinstance(p,MasteryPage) else p for p in dictionary["pages"]}

        # long # Summoner ID.
        self.summonerId = dictionary["summonerId"]


class MasteryPage(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Indicates if the mastery page is the current mastery page.
        self.current = dictionary["current"]

        # long # Mastery page ID.
        self.id = dictionary["id"]

        # list<MasteryDto> # Collection of masteries associated with the mastery page.
        self.masteries = dictionary["masteries"]

        # string # Mastery page name.
        self.name = dictionary["name"]


class Mastery(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Mastery ID. For static information correlating to masteries, please refer to the LoL Static Data API.
        self.id = dictionary["id"]

        # int # Mastery rank (i.e., the number of points put into this mastery).
        self.rank = dictionary["rank"]


class Summoner(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Summoner ID.
        self.id = dictionary["id"]

        # string # Summoner name.
        self.name = dictionary["name"]

        # int # ID of the summoner icon associated with the summoner.
        self.profileIconId = dictionary["profileIconId"]

        # long # Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change
        self.revisionDate = dictionary["revisionDate"]

        # long # Summoner level associated with the summoner.
        self.summonerLevel = dictionary["summonerLevel"]