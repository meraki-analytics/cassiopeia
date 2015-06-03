from datetime import datetime

from cassiopeia import riotapi
from cassiopeia.type.core.common import CassiopeiaObject, lazyproperty

class RunePage(CassiopeiaObject):
    def __str__(self):
        return "Rune Page ({name})".format(name=self.name)

    def __iter__(self):
        return iter(self.runes)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    @property
    def current(self):
        return self.dict.current

    @property
    def id(self):
        return self.dict.id

    @property
    def name(self):
        return self.dict.name

    @lazyproperty
    def runes(self):
        return riotapi.get_runes([slot.runeId for slot in self.data.slots])


class MasteryPage(CassiopeiaObject):
    def __str__(self):
        return "Mastery Page ({name})".format(name=self.name)

    def __iter__(self):
        return iter(self.masteries)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    @property
    def current(self):
        return self.dict.current

    @property
    def id(self):
        return self.dict.id

    @lazyproperty
    def masteries(self):
        masteries = []
        ranks = []
        for mastery in self.data.masteries:
            masteries.append(mastery.id)
            ranks.append(mastery.rank)
        return zip(riotapi.get_masteries(masteries), ranks)

    @property
    def name(self):
        return self.dict.name


class Summoner(CassiopeiaObject):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    # int # Summoner ID.
    @property
    def id(self):
        return self.data.id

    # str # Summoner name.
    @property
    def name(self):
        return self.data.name

    # int # ID of the summoner icon associated with the summoner.
    @property
    def profile_icon_id(self):
        return self.data.profileIconId

    # int # Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change
    @lazyproperty
    def modify_date(self):
        return datetime.utcfromtimestamp(self.data.revisionDate) if self.data.revisionDate else None

    # int # Summoner level associated with the summoner.
    @property
    def level(self):
        return self.data.summonerLevel