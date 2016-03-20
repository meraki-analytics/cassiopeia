import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.matchlist


@cassiopeia.type.core.common.inheritdocs
class MatchReference(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.matchlist.MatchReference

    def __str__(self):
        return "Match {id} Reference".format(id=self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @cassiopeia.type.core.common.immutablemethod
    def match(self, include_timeline=True):
        """
        Gets the full information for this match

        Args:
            include_timeline (bool): whether to include timeline data in the returned match

        Returns:
            Match: the match
        """
        return cassiopeia.riotapi.get_match(self, include_timeline)

    @cassiopeia.type.core.common.lazyproperty
    def champion(self):
        """
        Returns:
            Champion: the champion that the summoner played for the summoner that was used to pull this match reference
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.champion)

    @property
    def lane(self):
        """
        Returns:
            Lane: the lane that the summoner was in for the summoner that was used to  pull this match reference
        """
        lane = self.data.lane
        lane = "MIDDLE" if lane == "MID" else lane
        lane = "BOTTOM" if lane == "BOT" else lane
        return cassiopeia.type.core.common.Lane(lane) if lane else None

    @property
    def id(self):
        """
        Returns:
            int: the match id for this match
        """
        return self.data.matchId

    @property
    def platform(self):
        """
        Returns:
            Platform: the platform (ie server) for this match
        """
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

    @property
    def queue(self):
        """
        Returns:
            Queue: the queue type for this match
        """
        return cassiopeia.type.core.common.Queue(self.data.queue) if self.data.queue else None

    @property
    def role(self):
        """
        Returns:
            Role: the role that the summoner was in for the summoner that was used to  pull this match reference
        """
        return cassiopeia.type.core.common.Role(self.data.role) if self.data.role else None

    @property
    def season(self):
        """
        Returns:
            Season: the season that this match was played in
        """
        return cassiopeia.type.core.common.Season(self.data.season) if self.data.season else None

    @cassiopeia.type.core.common.lazyproperty
    def timestamp(self):
        """
        Returns:
            datetime: the timestamp for this match
        """
        return datetime.datetime.utcfromtimestamp(self.data.timestamp / 1000) if self.data.timestamp else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    MatchReference.dto_type = cassiopeia.type.dto.matchlist.MatchReference
