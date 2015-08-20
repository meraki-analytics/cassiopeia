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
    def match(self):
        """Gets the full information for this match

        return    Match    the match
        """
        return cassiopeia.riotapi.get_match(self)

    @cassiopeia.type.core.common.lazyproperty
    def champion(self):
        """Champion    the champion that the summoner played for the summoner that was used to pull this match reference"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.champion)

    @property
    def lane(self):
        """Lane    the lane that the summoner was in for the summoner that was used to  pull this match reference"""
        lane = self.data.lane
        lane = "MIDDLE" if lane == "MID" else lane
        lane = "BOTTOM" if lane == "BOT" else lane
        return cassiopeia.type.core.common.Lane(lane) if lane else None

    @property
    def id(self):
        """int    the match id for this match"""
        return self.data.matchId

    @property
    def platform(self):
        """Platform    the platform (ie server) for this match"""
        return cassiopeia.type.core.common.platform(self.data.platformid) if self.data.platformid else none

    @property
    def queue(self):
        """Queue    the queue type for this match"""
        return cassiopeia.type.core.common.queue(self.data.queue) if self.data.queue else none

    @property
    def role(self):
        """Role    the role that the summoner was in for the summoner that was used to  pull this match reference"""
        return cassiopeia.type.core.common.Role(self.data.role) if self.data.role else none

    @property
    def season(self):
        """Season    the season that this match was played in"""
        return cassiopeia.type.core.common.season(self.data.season) if self.data.season else none

    @cassiopeia.type.core.common.lazyproperty
    def timestamp(self):
        """datetime    the timestamp for this match"""
        return datetime.datetime.utcfromtimestamp(self.data.timestamp / 1000) if self.data.timestamp else none

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_rebind_all():
    MatchReference.dto_type = cassiopeia.type.dto.matchlist.MatchReference
