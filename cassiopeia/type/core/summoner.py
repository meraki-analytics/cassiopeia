import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common

class RunePage(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Rune Page ({name})".format(name=self.name)

    def __iter__(self):
        return iter(self.runes)

    def __len__(self):
        return len(self.runes)

    def __getitem__(self, index):
        return self.runes[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def current(self):
        return self.data.current

    @property
    def id(self):
        return self.data.id

    @property
    def name(self):
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        return cassiopeia.riotapi.get_runes([slot.runeId for slot in self.data.slots])


class MasteryPage(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Mastery Page ({name})".format(name=self.name)

    def __iter__(self):
        return iter(self.masteries)

    def __len__(self):
        return len(self.masteries)

    def __getitem__(self, index):
        return self.masteries[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def current(self):
        return self.data.current

    @property
    def id(self):
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        masteries = []
        ranks = []
        for mastery in self.data.masteries.items():
            masteries.append(mastery[0])
            ranks.append(mastery[1])
        return list(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def name(self):
        return self.data.name


class Summoner(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

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
    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        return datetime.datetime.utcfromtimestamp(self.data.revisionDate) if self.data.revisionDate else None

    # int # Summoner level associated with the summoner.
    @property
    def level(self):
        return self.data.summonerLevel