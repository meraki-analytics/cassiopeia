import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.summoner


@cassiopeia.type.core.common.inheritdocs
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
        """bool    whether or not this page is active"""
        return self.data.current

    @property
    def id(self):
        """int    the id of this summoner's rune page"""
        return self.data.id

    @property
    def name(self):
        """str    the name of this summoner's rune page"""
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        """list<Rune>    the runes in this rune page"""
        runes = {}
        for slot in self.data.slots:
            try:
                runes[slot.runeId] += 1
            except KeyError:
                runes[slot.runeId] = 1

        fetched = cassiopeia.riotapi.get_runes(list(runes.keys()))
        return {rune: runes[rune.id] for rune in fetched}


@cassiopeia.type.core.common.inheritdocs
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
        """bool    whether or not this mastery page is active"""
        return self.data.current

    @property
    def id(self):
        """int    the id of the mastery page for this summoner"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        """list<Mastery>    this mastery page's masteries"""
        masteries = []
        ranks = []
        for mastery in self.data.masteries.items():
            masteries.append(mastery[0])
            ranks.append(mastery[1])
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def name(self):
        """str    the name of this summoner's mastery page"""
        return self.data.name


@cassiopeia.type.core.common.inheritdocs
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
        """int    the summoner's id"""
        return self.data.id

    @property
    def name(self):
        """str    the summoner's name"""
        return self.data.name

    @property
    def profile_icon_id(self):
        """int    the ID of the summoner icon associated with the summoner"""
        return self.data.profileIconId

    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        """datetime    the date this summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: profile icon change, playing the tutorial or advanced tutorial, finishing a game, summoner name change"""
        return datetime.datetime.utcfromtimestamp(self.data.revisionDate / 1000) if self.data.revisionDate else None

    @property
    def level(self):
        """int    the Summoner's level"""
        return self.data.summonerLevel

    @cassiopeia.type.core.common.immutablemethod
    def current_game(self):
        """Gets the game the summoner is currently in, if they're in one

        return    Game    the game they're in (or None if they aren't in one)
        """
        return cassiopeia.riotapi.get_current_game(self)

    @cassiopeia.type.core.common.immutablemethod
    def recent_games(self):
        """Gets the most recent games the summoner played

        return    list<Game>    the summoner's recent games
        """
        return cassiopeia.riotapi.get_recent_games(self)

    @cassiopeia.type.core.common.immutablemethod
    def rune_pages(self):
        """Get the summoner's rune pages

        return    list<RunePage>    the summoner's rune pages
        """
        return cassiopeia.riotapi.get_rune_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def mastery_pages(self):
        """Get the summoner's mastery pages

        return    list<RunePage>    the summoner's mastery pages
        """
        return cassiopeia.riotapi.get_mastery_pages(self)

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        """Gets the leagues that the summoner belongs to. You probably don't want to call this with LoadPolicy.eager set.

        return    list<League>   the leagues that the summoner belongs to
        """
        return cassiopeia.riotapi.get_leagues_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        """Gets the leagues that the summoner belongs to, including only their own entries

        return    list<League>    the leagues that the summoner belongs to
        """
        return cassiopeia.riotapi.get_league_entries_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def teams(self):
        """Gets the summoner's' teams

        return    list<Team>    the summoner's teams
        """
        return cassiopeia.riotapi.get_teams_by_summoner(self)

    @cassiopeia.type.core.common.immutablemethod
    def match_list(self, num_matches=0, begin_index=0, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
        """Gets the summoner's match history

        num_matches     int                          the maximum number of matches to retrieve. 0 will get as many as possible. (default 0)
        begin_index     int                          the game index to start from (default 0)
        begin_time      int | datetime               the begin time to use for fetching games (default 0)
        end_time        int | datetime               the end time to use for fetching games (default 0)
        champions       Champion | list<Champion>    the champion(s) to limit the results to (default None)
        ranked_queue    Queue | list<Queue>          the ranked queue(s) to limit the results to (default None)
        seasons         Season | list<Season>        the season(s) to limit the results to (default None)

        return          list<MatchReference>         the summoner's match history
        """
        return cassiopeia.riotapi.get_match_list(self, num_matches, begin_index, begin_time, end_time, champions, ranked_queues, seasons)

    @cassiopeia.type.core.common.immutablemethod
    def ranked_stats(self, season=None):
        """Gets the summoner's ranked stats

        season    Season                             the season to get ranked stats for (None will give current season stats) (default None)

        return    dict<Champion, AggregatedStats>    the summoner's ranked stats divided by champion. The entry for None contains combined stats for all champions.
        """
        return cassiopeia.riotapi.get_ranked_stats(self, season)

    @cassiopeia.type.core.common.immutablemethod
    def stats(self, season=None):
        """Gets the summoner's stats

        season    Season                                 the season to get stats for (None will give current season stats) (default None)

        return    dict<StatSummaryType, StatsSummary>    the summoner's stats divided by queue type
        """
        return cassiopeia.riotapi.get_stats(self, season)


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    RunePage.dto_type = cassiopeia.type.dto.summoner.RunePage
    MasteryPage.dto_type = cassiopeia.type.dto.summoner.MasteryPage
    Summoner.dto_type = cassiopeia.type.dto.summoner.Summoner
