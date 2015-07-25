import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.summoner

class RunePage(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.summoner.RunePage

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
        runes = {}
        for slot in self.data.slots:
            try:
                runes[slot.runeId] += 1
            except(KeyError):
                runes[slot.runeId] = 1

        fetched = cassiopeia.riotapi.get_runes(list(runes.keys()))
        return {rune: runes[rune.id] for rune in fetched}

class MasteryPage(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.summoner.MasteryPage

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
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def name(self):
        return self.data.name


class Summoner(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.summoner.Summoner

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
        return datetime.datetime.utcfromtimestamp(self.data.revisionDate / 1000) if self.data.revisionDate else None

    # int # Summoner level associated with the summoner.
    @property
    def level(self):
        return self.data.summonerLevel

    @cassiopeia.type.core.common.immutablemethod
    def rune_pages(self):
        return cassiopeia.riotapi.get_rune_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def mastery_pages(self):
        return cassiopeia.riotapi.get_mastery_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        return cassiopeia.riotapi.get_leagues_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        return cassiopeia.riotapi.get_league_entries_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def match_history(self, begin_index=0, champions=None, ranked_queues=None):
        return cassiopeia.riotapi.get_match_history(self, begin_index, champions, ranked_queues)

    @cassiopeia.type.core.common.immutablemethod
    def match_list(self, begin_index=0, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
        return cassiopeia.riotapi.get_match_list(self, begin_index, begin_time, end_time, champions, ranked_queues, seasons)

    @cassiopeia.type.core.common.immutablemethod
    def ranked_stats(self, season=None):
        return cassiopeia.riotapi.get_ranked_stats(self, season)

    @cassiopeia.type.core.common.immutablemethod
    def stats(self, season=None):
        return cassiopeia.riotapi.get_stats(self, season)