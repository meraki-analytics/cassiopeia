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
class TournamentParameters(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.TournamentCodeParameters

    """
    team_size            int               the team size for the tournament (1-5)
    spectator_type       SpectatorType     the spectator availability for the tournament
    pick_type            PickType          the pick type for the tournament
    map_type             MapType           the map the tournament is played on
    allowed_summoners    list<Summoner>    the summoners who are allowed to participate in the tournament
    meta_data            str | object      meta data to be included with the tournament. Any non-string value will be cast to a string.
    """
    def __init__(self, team_size, spectator_type, pick_type, map_type, allowed_summoners=[], meta_data=""):
        if team_size < 1 or team_size > 5:
            raise ValueError("Team Size must be between 1 and 5!")

        summoners = cassiopeia.type.dto.tournament.SummonerIdParams([summoner.id for summoner in allowed_summoners]) if allowed_summoners else None
        self.data = cassiopeia.type.dto.tournament.TournamentCodeParameters(team_size, spectator_type.value, pick_type.value, map_type.value, summoners, str(meta_data))

    @property
    def team_size(self):
        """int    the team size for the tournament (1-5)"""
        return self.data.teamSize

    @team_size.setter
    def team_size(self, value):
        if value < 1 or value > 5:
            raise ValueError("Team Size must be between 1 and 5!")
        self.data.teamSize = value

    @property
    def spectator_type(self):
        """SpectatorType    the spectator availability for the tournament"""
        return SpectatorType(self.data.spectatorType)

    @spectator_type.setter
    def spectator_type(self, value):
        self.data.spectatorType = value.value

    @property
    def pick_type(self):
        """PickType    the pick type for the tournament"""
        return PickType(self.data.pickType)

    @pick_type.setter
    def pick_type(self, value):
        self.data.pickType = value.value

    @property
    def map_type(self):
        """MapType    the map the tournament is played on"""
        return MapType(self.data.mapType)

    @map_type.setter
    def map_type(self, value):
        self.data.mapType = value.value

    @property
    def allowed_summoners(self):
        """list<Summoner>    the summoners who are allowed to participate in the tournament"""
        return cassiopeia.riotapi.get_summoners_by_id(self.data.allowedSummonerIds.participants) if self.data.allowedSummonerIds else []

    @allowed_summoners.setter
    def allowed_summoners(self, value):
        if not value:
            self.data.allowedSummonerIds = None
            return

        if not self.data.allowedSummonerIds and value:
            self.data.allowedSummonerIds = cassiopeia.type.dto.tournament.SummonerIdParams([])
        self.data.allowedSummonerIds.participants = [summoner.id for summoner in value]

    @allowed_summoners.deleter
    def allowed_summoners(self):
        self.data.allowedSummonerIds = None

    @property
    def meta_data(self):
        """str    meta data to be included with the tournament. Any non-string value will be cast to a string."""
        return self.data.metadata

    @meta_data.setter
    def meta_data(self, value):
        self.data.metadata = str(value)

    @meta_data.deleter
    def meta_data(self):
        self.data.metadata = ""


@cassiopeia.type.core.common.inheritdocs
class TournamentLobby(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.TournamentCode

    def __str__(self):
        return "{name} ({code})".format(name=self.name, code=self.code)

    @property
    def code(self):
        """str    the tournament code"""
        return self.data.code

    @property
    def id(self):
        """int    the tournament code's ID"""
        return self.data.id

    @property
    def name(self):
        """str    the lobby name"""
        return self.data.lobbyName

    @property
    def map(self):
        """str    the map for the game"""
        return MapType(self.data.map) if self.data.map else None

    @property
    def meta_data(self):
        """str    the metadata for the game"""
        return self.data.metaData

    @property
    def participants(self):
        """list<Summoner>    the summoners participating in the tournament"""
        return cassiopeia.riotapi.get_summoners_by_id(self.data.participants) if self.data.participants else []

    @property
    def password(self):
        """str    the password for the lobby"""
        return self.data.password

    @property
    def pick_type(self):
        """PickType    the pick mode for the game"""
        return PickType(self.data.pickType) if self.data.pickType else None

    @property
    def provider_id(self):
        """int    the provider's ID"""
        return self.data.providerId

    @property
    def region(self):
        """TournamentRegion    the tournament's region"""
        return TournamentRegion(self.data.region) if self.data.region else None

    @property
    def spectator_type(self):
        """SpectatorType    the spectator mode for the game"""
        return SpectatorType(self.data.spectators) if self.data.spectators else None

    @property
    def team_size(self):
        """int    the team size for the game"""
        return self.data.teamSize

    @property
    def tournament_id(self):
        """int    the tournament's ID"""
        return self.data.tournamentId


@cassiopeia.type.core.common.inheritdocs
class TournamentUpdateParameters(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.TournamentCodeUpdateParameters

    """
    allowed_summoners    list<Summoner>    the summoners who are allowed to participate in the tournament
    spectator_type       SpectatorType     the spectator availability for the tournament
    pick_type            PickType          the pick type for the tournament
    map_type             MapType           the map the tournament is played on
    """
    def __init__(self, allowed_summoners=[], spectator_type=None, pick_type=None, map_type=None):
        summoners = ",".join([str(summoner.id) for summoner in allowed_summoners])
        self.data = cassiopeia.type.dto.tournament.TournamentCodeUpdateParameters(summoners, spectator_type.value if spectator_type else "", pick_type.value if pick_type else "", map_type.value if map_type else "")

    @property
    def allowed_summoners(self):
        """list<Summoner>    the summoners who are allowed to participate in the tournament"""
        ids = [int(id_) for id_ in self.data.allowedParticipants.split(",") if id_]
        return cassiopeia.riotapi.get_summoners_by_id(ids)

    @allowed_summoners.setter
    def allowed_summoners(self, value):
        self.data.allowedParticipants = ",".join([str(summoner.id) for summoner in value])

    @allowed_summoners.deleter
    def allowed_summoners(self):
        self.data.allowedParticipants = ""

    @property
    def spectator_type(self):
        """SpectatorType    the spectator availability for the tournament"""
        return SpectatorType(self.data.spectatorType)

    @spectator_type.setter
    def spectator_type(self, value):
        self.data.spectatorType = value.value if value else ""

    @spectator_type.deleter
    def spectator_type(self):
        self.data.spectatorType = ""

    @property
    def pick_type(self):
        """PickType    the pick type for the tournament"""
        return PickType(self.data.pickType)

    @pick_type.setter
    def pick_type(self, value):
        self.data.pickType = value.value if value else ""

    @pick_type.deleter
    def pick_type(self):
        self.data.pickType = ""

    @property
    def map_type(self):
        """MapType    the map the tournament is played on"""
        return MapType(self.data.mapType)

    @map_type.setter
    def map_type(self, value):
        self.data.mapType = value.value if value else ""

    @map_type.deleter
    def map_type(self):
        self.data.mapType = ""


@cassiopeia.type.core.common.inheritdocs
class LobbyEvent(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.LobbyEvent

    def __str__(self):
        return "{type} ({summoner})".format(type=self.type, summoner=self.summoner)

    @property
    def type(self):
        """str    the type of the event"""
        return self.data.eventType

    @property
    def summoner(self):
        """Summoner    the summoner that triggered the event"""
        return cassiopeia.riotapi.get_summoner_by_id(int(self.data.summonerId)) if self.data.summonerId else None

    @property
    def timestamp(self):
        """str    the time that the event occurred"""
        return self.data.timestamp


@cassiopeia.type.core.common.inheritdocs
class ProviderRegistrationParameters(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.ProviderRegistrationParameters

    """
    region    TournamentRegion    the region in which the provider will be running tournaments
    url       str                 the provider's callback URL to which tournament game results in this region should be posted. The URL must be well-formed, use the http or https protocol, and use the default port for the protocol (http URLs must use port 80, https URLs must use port 443).
    """
    def __init__(self, region, url):
        self.data = cassiopeia.type.dto.tournament.ProviderRegistrationParameters(region.value, url)

    @property
    def region(self):
        """TournamentRegion    the region in which the provider will be running tournaments"""
        return TournamentRegion(self.data.region)

    @region.setter
    def region(self, value):
        self.data.region = value.value

    @property
    def url(self):
        """str    the provider's callback URL to which tournament game results in this region should be posted. The URL must be well-formed, use the http or https protocol, and use the default port for the protocol (http URLs must use port 80, https URLs must use port 443)."""
        return self.data.url

    @url.setter
    def url(self, value):
        self.data.url = value


@cassiopeia.type.core.common.inheritdocs
class TournamentRegistrationParameters(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.tournament.TournamentRegistrationParameters

    """
    provider_id    int    the provider ID to specify the regional registered provider data to associate this tournament
    name           str    the optional name of the tournament
    """
    def __init__(self, provider_id, name=""):
        self.data = cassiopeia.type.dto.tournament.TournamentRegistrationParameters(provider_id, name)

    @property
    def provider_id(self):
        """int    the provider ID to specify the regional registered provider data to associate this tournament"""
        return self.data.providerId

    @provider_id.setter
    def provider_id(self, value):
        self.data.providerId = value

    @property
    def name(self):
        """str    the optional name of the tournament"""
        return self.data.name

    @name.setter
    def name(self, value):
        self.data.name = value

    @name.deleter
    def name(self):
        self.data.name = ""
