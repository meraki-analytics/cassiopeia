import cassiopeia.type.dto.common
import cassiopeia.type.core.common


@cassiopeia.type.core.common.inheritdocs
class TournamentCodeParameters(cassiopeia.type.dto.common.CassiopeiaParametersDto):
    """
    teamSize              int                 the team size of the game. Valid values are 1-5.
    spectatorType         str                 the spectator type of the game. Valid values are NONE, LOBBYONLY, ALL.
    pickType              str                 the pick type of the game. Valid values are BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT.
    mapType               str                 the map type of the game. Valid values are SUMMONERS_RIFT, TWISTED_TREELINE, CRYSTAL_SCAR, and HOWLING_ABYSS.
    allowedSummonerIds    SummonerIdParams    optional list of participants in order to validate the players eligible to join the lobby. NOTE: We currently do not enforce participants at the team level, but rather the aggregate of teamOne and teamTwo. We may add the ability to enforce at the team level in the future.
    metadata              str                 optional string that may contain any data in any format, if specified at all. Used to denote any custom information about the game.
    """
    def __init__(self, teamSize, spectatorType, pickType, mapType, allowedSummonerIds=None, metadata=""):
        self.teamSize = teamSize
        self.spectatorType = spectatorType
        self.pickType = pickType
        self.mapType = mapType
        self.allowedSummonerIds = allowedSummonerIds
        self.metadata = metadata


@cassiopeia.type.core.common.inheritdocs
class SummonerIdParams(cassiopeia.type.dto.common.CassiopeiaParametersDto):
    """
    participants    list<int>   the tournament participants
    """
    def __init__(self, participants):
        self.participants = participants


@cassiopeia.type.core.common.inheritdocs
class TournamentCode(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    code            str          the tournament code
    id              int          the tournament code's ID
    lobbyName       str          the lobby name for the tournament code game
    map             str          the game map for the tournament code game
    metaData        str          the metadata for tournament code
    participants    list<int>    the IDs of the summoners participating in the tournament
    password        str          the password for the tournament code game
    pickType        str          the pick mode for tournament code game
    providerId      int          the provider's ID
    region          str          the tournament code's region (Legal values: BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, PBE, RU, TR)
    spectators      str          the spectator mode for the tournament code game
    teamSize        int          the team size for the tournament code game
    tournamentId    int          the tournament's ID
    """
    def __init__(self, dictionary):
        self.code = dictionary.get("code", "")
        self.id = dictionary.get("id", 0)
        self.lobbyName = dictionary.get("lobbyName", "")
        self.map = dictionary.get("map", "")
        self.metaData = dictionary.get("metaData", "")
        self.participants = dictionary.get("participants", [])
        self.password = dictionary.get("password", "")
        self.pickType = dictionary.get("pickType", "")
        self.providerId = dictionary.get("providerId", 0)
        self.region = dictionary.get("region", "")
        self.spectators = dictionary.get("spectators", "")
        self.teamSize = dictionary.get("teamSize", 0)
        self.tournamentId = dictionary.get("tournamentId", 0)


@cassiopeia.type.core.common.inheritdocs
class TournamentCodeUpdateParameters(cassiopeia.type.dto.common.CassiopeiaParametersDto):
    """
    allowedParticipants    str    comma separated list of summoner Ids
    spectatorType          str    the spectator type (Legal values: NONE, LOBBYONLY, ALL)
    pickType               str    the pick type (Legal values: BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT)
    mapType                str    the map type (Legal values: SUMMONERS_RIFT, CRYSTAL_SCAR, TWISTED_TREELINE, HOWLING_ABYSS)
    """
    def __init__(self, allowedParticipants="", spectatorType="", pickType="", mapType=""):
        self.allowedParticipants = allowedParticipants
        self.spectatorType = spectatorType
        self.pickType = pickType
        self.mapType = mapType


@cassiopeia.type.core.common.inheritdocs
class LobbyEventWrapper(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    eventList    list<LobbyEvent>    the list of events
    """
    def __init__(self, dictionary):
        self.eventList = [(LobbyEvent(event) if not isinstance(event, LobbyEvent) else event) for event in dictionary.get("eventList", []) if event]
        self.eventList.sort(key=lambda e: e.timestamp)


@cassiopeia.type.core.common.inheritdocs
class LobbyEvent(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    eventType     str    the type of event that was triggered
    summonerId    str    the summoner that triggered the event
    timestamp     str    timestamp from the event
    """
    def __init__(self, dictionary):
        self.eventType = dictionary.get("eventType", "")
        self.summonerId = dictionary.get("summonerId", 0)
        self.timestamp = dictionary.get("timestamp", 0)


@cassiopeia.type.core.common.inheritdocs
class ProviderRegistrationParameters(cassiopeia.type.dto.common.CassiopeiaParametersDto):
    """
    region    str    the region in which the provider will be running tournaments (Legal values: BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, PBE, RU, TR)
    url       str    the provider's callback URL to which tournament game results in this region should be posted. The URL must be well-formed, use the http or https protocol, and use the default port for the protocol (http URLs must use port 80, https URLs must use port 443).
    """
    def __init__(self, region, url):
        self.region = region
        self.url = url


@cassiopeia.type.core.common.inheritdocs
class TournamentRegistrationParameters(cassiopeia.type.dto.common.CassiopeiaParametersDto):
    """
    providerId    int    the provider ID to specify the regional registered provider data to associate this tournament
    name          str    the optional name of the tournament
    """
    def __init__(self, providerId, name=""):
        self.providerId = providerId
        self.name = name
