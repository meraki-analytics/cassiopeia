import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.league


@cassiopeia.type.core.common.inheritdocs
class Series(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.MiniSeries

    def __str__(self):
        return self.progress

    @property
    def losses(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.losses

    @property
    def progress(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.progress

    @property
    def wins_required(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.target

    @property
    def wins(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class Entry(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.LeagueEntry

    def __str__(self):
        return "{summoner} ({lp} LP)".format(summoner=self.summoner_name, lp=self.league_points)

    @property
    def division(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return cassiopeia.type.core.common.Division(self.data.division) if self.data.division else None

    @property
    def fresh_blood(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.isFreshBlood

    @property
    def hot_streak(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.isHotStreak

    @property
    def inactive(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.isInactive

    @property
    def veteran(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.isVeteran

    @property
    def league_points(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.leaguePoints

    @property
    def losses(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.losses

    @cassiopeia.type.core.common.lazyproperty
    def series(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return Series(self.data.miniSeries) if self.data.miniSeries else None

    @property
    def summoner(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        if not self.data.playerOrTeamId:
            return None

        try:
            id_ = int(self.data.playerOrTeamId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except ValueError:
            return None

    @property
    def team(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        if not self.data.playerOrTeamId:
            return None

        try:
            int(self.data.playerOrTeamId)
            return None
        except ValueError:
            return cassiopeia.riotapi.get_team_by_id(self.data.playerOrTeamId)

    @property
    def summoner_name(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        if not self.data.playerOrTeamId:
            return ""

        try:
            int(self.data.playerOrTeamId)
            return self.data.playerOrTeamName
        except ValueError:
            return ""

    @property
    def team_name(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        try:
            int(self.data.playerOrTeamId)
            return ""
        except ValueError:
            return self.data.playerOrTeamName

    @property
    def wins(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class League(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.league.League

    def __str__(self):
        return "{name} ({tier})".format(name=self.name, tier=self.tier)

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    @cassiopeia.type.core.common.lazyproperty
    def entries(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return sorted([Entry(entry) for entry in self.data.entries], key=lambda entry: entry.league_points, reverse=True)

    @property
    def name(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def participant_entry(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        for entry in self.entries:
            if entry.data.playerOrTeamId == self.data.participantId:
                return entry
        return None

    @property
    def summoner(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        if not self.data.participantId:
            return None

        try:
            id_ = int(self.data.participantId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except ValueError:
            return None

    @property
    def team(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        if not self.data.participantId:
            return None

        try:
            int(self.data.participantId)
            return None
        except ValueError:
            return cassiopeia.riotapi.get_team_by_id(self.data.participantId)

    @property
    def queue(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return cassiopeia.type.core.common.Queue(self.data.queue) if self.data.queue else None

    @property
    def tier(self):
        """
        Returns:
            int: number of current losses in the mini series
        """
        return cassiopeia.type.core.common.Tier(self.data.tier) if self.data.tier else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Series.dto_type = cassiopeia.type.dto.league.MiniSeries
    Entry.dto_type = cassiopeia.type.dto.league.LeagueEntry
    League.dto_type = cassiopeia.type.dto.league.League
