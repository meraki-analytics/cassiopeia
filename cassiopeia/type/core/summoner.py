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
        """Whether or not this page is active"""
        return self.data.current

    @property
    def id(self):
        """The ID of this summoner's rune page"""
        return self.data.id

    @property
    def name(self):
        """The name of this summoner's rune page"""
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        """The runes in this rune page"""
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
        """Whether or not this mastery page is active"""
        return self.data.current

    @property
    def id(self):
        """The ID of the mastery page for this summoner"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        """This mastery page's masteries"""
        masteries = []
        ranks = []
        for mastery in self.data.masteries.items():
            masteries.append(mastery[0])
            ranks.append(mastery[1])
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def name(self):
        """The name of this summoner's mastery page"""
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

    @property
    def id(self):
        """The Summoner's ID"""
        return self.data.id

    @property
    def name(self):
        """The Summoner's name"""
        return self.data.name

    @property
    def profile_icon_id(self):
        """The ID of the summoner icon associated with the summoner"""
        return self.data.profileIconId

    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        """The date this summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change"""
        return datetime.datetime.utcfromtimestamp(self.data.revisionDate / 1000) if self.data.revisionDate else None

    @property
    def level(self):
        """The Summoner's level"""
        return self.data.summonerLevel

    @cassiopeia.type.core.common.immutablemethod
    def current_game(self):
        """Returns the Summoner's current game, if any"""
        return cassiopeia.riotapi.get_current_game(self)

    @cassiopeia.type.core.common.immutablemethod
    def recent_games(self):
        """Returns the Summoner's recent games, if any"""
        return cassiopeia.riotapi.get_recent_games(self)

    @cassiopeia.type.core.common.immutablemethod
    def rune_pages(self):
        """Returns the Summoner's rune pages, if any"""
        return cassiopeia.riotapi.get_rune_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def mastery_pages(self):
        """Returns the Summoner's mastery pages, if any"""
        return cassiopeia.riotapi.get_mastery_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        """Returns the Summoner's League"""
        return cassiopeia.riotapi.get_leagues_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        """Returns the Summoner's league Entries"""
        return cassiopeia.riotapi.get_league_entries_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def teams(self):
        """Gets the Summoner's teams"""
        return cassiopeia.riotapi.get_teams_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def match_history(self, begin_index=0, champions=None, ranked_queues=None):
        """Gets the Summoner's match history

        begin_index      int               the first index of games in the summoner's history that you want to start pulling (default 0)
        champions        list<Champion>    a list of champions you want to get games for (default None)
        ranked_queues    Enum              the ranked queues you want to pull (default None)

        return    list<MatchHistory>
        """
        return cassiopeia.riotapi.get_match_history(self, begin_index, champions, ranked_queues)

    @cassiopeia.type.core.common.immutablemethod
    def match_list(self, begin_index=-1, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
        """Gets the Summoner's match history

        begin_index      int               the first index of games in the summoner's history that you want to start pulling (default -1)
        begin_time       int               epoch time for when you want to start pulling the summoner's matches (default 0)
        end_time         int               epoch time for when you want to stop pulling the summoner's matches (default 0)
        champions        list<Champion>    a list of champions you want to get games for (default None)
        ranked_queues    Enum              the ranked queues you want to pull (default None)

        return    list<MatchHistory>
        """
        return cassiopeia.riotapi.get_match_list(self, begin_index, begin_time, end_time, champions, ranked_queues, seasons)

    @cassiopeia.type.core.common.immutablemethod
    def ranked_stats(self, season=None):
        """Gets the ranked statistics for this summoner

        season    Enum    the season you want to pull the summoner's stats for (default None)

        return    StatsSummary
        """
        return cassiopeia.riotapi.get_ranked_stats(self, season)

    @cassiopeia.type.core.common.immutablemethod
    def stats(self, season=None):
        """Gets the overall statistics for this summoner

        season    Enum    the season you want to pull the summoner's stats for (default None)

        return    StatsSummary
        """
        return cassiopeia.riotapi.get_stats(self, season)

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    RunePage.dto_type = cassiopeia.type.dto.summoner.RunePage
    MasteryPage.dto_type = cassiopeia.type.dto.summoner.MasteryPage
    Summoner.dto_type = cassiopeia.type.dto.summoner.Summoner
