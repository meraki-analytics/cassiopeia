import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class Participant(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "FeaturedGameParticipant"
    bot = sqlalchemy.Column(sqlalchemy.Boolean)
    championId = sqlalchemy.Column(sqlalchemy.Integer)
    profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
    spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
    spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
    summonerName = sqlalchemy.Column(sqlalchemy.String(30))
    teamId = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId"))

    def __init__(self, dictionary):
        # bool # Flag indicating whether or not this participant is a bot
        self.bot = dictionary.get("bot", False)

        # int # The ID of the champion played by this participant
        self.championId = dictionary.get("championId", 0)

        # int # The ID of the profile icon used by this participant
        self.profileIconId = dictionary.get("profileIconId", 0)

        # int # The ID of the first summoner spell used by this participant
        self.spell1Id = dictionary.get("spell1Id", 0)

        # int # The ID of the second summoner spell used by this participant
        self.spell2Id = dictionary.get("spell2Id", 0)

        # str # The summoner name of this participant
        self.summonerName = dictionary.get("summonerName", "")

        # int # The team ID of this participant, indicating the participant's team
        self.teamId = dictionary.get("teamId", 0)


class Observer(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "FeaturedGameObserver"
    encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId"))

    def __init__(self, dictionary):
        # str # Key used to decrypt the spectator grid game data for playback
        self.encryptionKey = dictionary.get("encryptionKey", "")


class BannedChampion(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "FeaturedGameBannedChampion"
    championId = sqlalchemy.Column(sqlalchemy.Integer)
    pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
    teamId = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId"))

    def __init__(self, dictionary):
        # int # The ID of the banned champion
        self.championId = dictionary.get("championId", 0)

        # int # The turn during which the champion was banned
        self.pickTurn = dictionary.get("pickTurn", 0)

        # int # The ID of the team that banned the champion
        self.teamId = dictionary.get("teamId", 0)


class FeaturedGameInfo(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "FeaturedGameInfo"
    bannedChampions = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
    gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    gameLength = sqlalchemy.Column(sqlalchemy.Integer)
    gameMode = sqlalchemy.Column(sqlalchemy.String(30))
    gameQueueConfigId = sqlalchemy.Column(sqlalchemy.Integer)
    gameStartTime = sqlalchemy.Column(sqlalchemy.Integer)
    gameType = sqlalchemy.Column(sqlalchemy.String(30))
    mapId = sqlalchemy.Column(sqlalchemy.Integer)
    observers = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.Observer", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.FeaturedGameParticipant", cascade="all, delete-orphan", passive_deletes=True)
    platformId = sqlalchemy.Column(sqlalchemy.String(30))

    def __init__(self, dictionary):
        # list<BannedChampion> # Banned champion information
        self.bannedChampions = [(BannedChampion(ban) if not isinstance(ban, BannedChampion) else ban) for ban in dictionary.get("bannedChampions", []) if ban]

        # int # The ID of the game
        self.gameId = dictionary.get("gameId", 0)

        # int # The amount of time in seconds that has passed since the game started
        self.gameLength = dictionary.get("gameLength", 0)

        # str # The game mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.gameMode = dictionary.get("gameMode", "")

        # int # The queue type (queue types are documented on the Game Constants page)
        self.gameQueueConfigId = dictionary.get("gameQueueConfigId", 0)

        # int # The game start time represented in epoch milliseconds
        self.gameStartTime = dictionary.get("gameStartTime", 0)

        # str # The game type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.gameType = dictionary.get("gameType", "")

        # int # The ID of the map
        self.mapId = dictionary.get("mapId", 0)

        # Observer # The observer information
        val = dictionary.get("observers", None)
        self.observers = Observer(val) if val and not isinstance(val, Observer) else val

        # list<Participant> # The participant information
        self.participants = [(Participant(participant) if not isinstance(participant, BannedChampion) else participant) for participant in dictionary.get("participants", []) if participant]

        # str # The ID of the platform on which the game is being played
        self.platformId = dictionary.get("platformId", "")


class FeaturedGames(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # The suggested interval to wait before requesting FeaturedGames again
        self.clientRefreshInterval = dictionary.get("clientRefreshInterval", 0)

        # list<FeaturedGameInfo> # The list of featured games
        self.gameList = [(FeaturedGameInfo(game) if not isinstance(game, FeaturedGameInfo) else game) for game in dictionary.get("gameList", []) if game]