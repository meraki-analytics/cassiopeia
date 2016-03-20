import enum

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.tournament


class MapType(enum.Enum):
    summoners_rift = "SUMMONERS_RIFT"
    twisted_treeline = "TWISTED_TREELINE"
    crystal_scar = "CRYSTAL_SCAR"
    howling_abyss = "HOWLING_ABYSS"


class PickType(enum.Enum):
    blind = "BLIND_PICK"
    draft = "DRAFT_MODE"
    random = "ALL_RANDOM"
    tournament_draft = "TOURNAMENT_DRAFT"


class SpectatorType(enum.Enum):
    none = "NONE"
    lobby = "LOBBYONLY"
    all = "ALL"


class TournamentRegion(enum.Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    pbe = "PBE"
    russia = "RU"
    turkey = "TR"


@cassiopeia.type.core.common.inheritdocs
class TournamentCode(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.TournamentCode

    def __str__(self):
        return "{name} ({code})".format(name=self.name, code=self.code)

    @property
    def code(self):
        """
        Returns:
            str: the tournament code
        """
        return self.data.code

    @property
    def id(self):
        """
        Returns:
            int: the tournament code's ID
        """
        return self.data.id

    @property
    def name(self):
        """
        Returns:
            str: the lobby name
        """
        return self.data.lobbyName

    @property
    def map(self):
        """
        Returns:
            str: the map for the game
        """
        return MapType(self.data.map) if self.data.map else None

    @property
    def meta_data(self):
        """
        Returns:
            str: the metadata for the game
        """
        return self.data.metaData

    @property
    def participants(self):
        """
        Returns:
            list<Summoner>: the summoners participating in the tournament
        """
        return cassiopeia.riotapi.get_summoners_by_id(self.data.participants) if self.data.participants else []

    @property
    def password(self):
        """
        Returns:
            str: the password for the lobby
        """
        return self.data.password

    @property
    def pick_type(self):
        """
        Returns:
            PickType: the pick mode for the game
        """
        return PickType(self.data.pickType) if self.data.pickType else None

    @property
    def provider_id(self):
        """
        Returns:
            int: the provider's ID
        """
        return self.data.providerId

    @property
    def region(self):
        """
        Returns:
            TournamentRegion: the tournament's region
        """
        return TournamentRegion(self.data.region) if self.data.region else None

    @property
    def spectator_type(self):
        """
        Returns:
            SpectatorType: the spectator mode for the game
        """
        return SpectatorType(self.data.spectators) if self.data.spectators else None

    @property
    def team_size(self):
        """
        Returns:
            int: the team size for the game
        """
        return self.data.teamSize

    @property
    def tournament_id(self):
        """
        Returns:
            int: the tournament's ID
        """
        return self.data.tournamentId


@cassiopeia.type.core.common.inheritdocs
class LobbyEvent(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.LobbyEvent

    def __str__(self):
        return "{type} ({summoner})".format(type=self.type, summoner=self.summoner)

    @property
    def type(self):
        """
        Returns:
            str: the type of the event
        """
        return self.data.eventType

    @property
    def summoner(self):
        """
        Returns:
            Summoner: the summoner that triggered the event
        """
        return cassiopeia.riotapi.get_summoner_by_id(int(self.data.summonerId)) if self.data.summonerId else None

    @property
    def timestamp(self):
        """
        Returns:
            str: the time that the event occurred
        """
        return self.data.timestamp


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    TournamentCode.dto_type = cassiopeia.type.dto.tournament.TournamentCode
    LobbyEvent.dto_type = cassiopeia.type.dto.tournament.LobbyEvent
