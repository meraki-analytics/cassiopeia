import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        bot (bool): flag indicating whether or not this participant is a bot
        championId (int): the ID of the champion played by this participant
        profileIconId (int): the ID of the profile icon used by this participant
        spell1Id (int): the ID of the first summoner spell used by this participant
        spell2Id (int): the ID of the second summoner spell used by this participant
        summonerName (str): the summoner name of this participant
        teamId (int): the team ID of this participant, indicating the participant's team
        encryptionKey (str): key used to decrypt the spectator grid game data for playback
        championId (int): the ID of the banned champion
        pickTurn (int): the turn during which the champion was banned
        teamId (int): the ID of the team that banned the champion
    """
    def __init__(self, dictionary):
        self.bot = dictionary.get("bot", False)
        self.championId = dictionary.get("championId", 0)
        self.profileIconId = dictionary.get("profileIconId", 0)
        self.spell1Id = dictionary.get("spell1Id", 0)
        self.spell2Id = dictionary.get("spell2Id", 0)
        self.summonerName = dictionary.get("summonerName", "")
        self.teamId = dictionary.get("teamId", 0)


@cassiopeia.type.core.common.inheritdocs
class Observer(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        encryptionKey (str): key used to decrypt the spectator grid game data for playback
    """
    def __init__(self, dictionary):
        self.encryptionKey = dictionary.get("encryptionKey", "")


@cassiopeia.type.core.common.inheritdocs
class BannedChampion(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        championId (int): the ID of the banned champion
        pickTurn (int): the turn during which the champion was banned
        teamId (int): the ID of the team that banned the champion
    """
    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.pickTurn = dictionary.get("pickTurn", 0)
        self.teamId = dictionary.get("teamId", 0)


@cassiopeia.type.core.common.inheritdocs
class FeaturedGameInfo(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        bannedChampions (list<BannedChampion>): banned champion information
        gameId (int): the ID of the game
        gameLength (int): the amount of time in seconds that has passed since the game started
        gameMode (str): the game mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        gameQueueConfigId (int): the queue type (queue types are documented on the Game Constants page)
        gameStartTime (int): the game start time represented in epoch milliseconds
        gameType (str): the game type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        mapId (int): the ID of the map
        observers (Observer): the observer information
        participants (list<Participant>): the participant information
        platformId (str): the ID of the platform on which the game is being played
    """
    def __init__(self, dictionary):
        self.bannedChampions = [(BannedChampion(ban) if not isinstance(ban, BannedChampion) else ban) for ban in dictionary.get("bannedChampions", []) if ban]
        self.gameId = dictionary.get("gameId", 0)
        self.gameLength = dictionary.get("gameLength", 0)
        self.gameMode = dictionary.get("gameMode", "")
        self.gameQueueConfigId = dictionary.get("gameQueueConfigId", 0)
        self.gameStartTime = dictionary.get("gameStartTime", 0)
        self.gameType = dictionary.get("gameType", "")
        self.mapId = dictionary.get("mapId", 0)
        val = dictionary.get("observers", None)
        self.observers = Observer(val) if val and not isinstance(val, Observer) else val
        self.participants = [(Participant(participant) if not isinstance(participant, BannedChampion) else participant) for participant in dictionary.get("participants", []) if participant]
        self.platformId = dictionary.get("platformId", "")

    @property
    def champion_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for ban in self.bannedChampions:
            ids.add(ban.championId)
        for p in self.participants:
            ids.add(p.championId)
        return ids

    @property
    def summoner_spell_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for p in self.participants:
            if p.spell1Id:
                ids.add(p.spell1Id)
            if p.spell2Id:
                ids.add(p.spell2Id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class FeaturedGames(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all champion IDs contained in this object
    """
    def __init__(self, dictionary):
        self.clientRefreshInterval = dictionary.get("clientRefreshInterval", 0)
        self.gameList = [(FeaturedGameInfo(game) if not isinstance(game, FeaturedGameInfo) else game) for game in dictionary.get("gameList", []) if game]

    @property
    def champion_ids(self):
        """
        Gets all summoner spell IDs contained in this object
        """
        ids = set()
        for game in self.gameList:
            ids |= game.champion_ids
        return ids

    @property
    def summoner_spell_ids(self):
        """
        Gets all summoner spell IDs contained in this object
        """
        ids = set()
        for game in self.gameList:
            ids |= game.summoner_spell_ids
        return ids


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_participant():
    global Participant

    @cassiopeia.type.core.common.inheritdocs
    class Participant(Participant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameParticipant"
        bot = sqlalchemy.Column(sqlalchemy.Boolean)
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_observer():
    global Observer

    @cassiopeia.type.core.common.inheritdocs
    class Observer(Observer, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameObserver"
        encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_banned_champion():
    global BannedChampion

    @cassiopeia.type.core.common.inheritdocs
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_featured_game_info():
    global FeaturedGameInfo

    @cassiopeia.type.core.common.inheritdocs
    class FeaturedGameInfo(FeaturedGameInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameInfo"
        bannedChampions = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
        gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        gameLength = sqlalchemy.Column(sqlalchemy.Integer)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        gameQueueConfigId = sqlalchemy.Column(sqlalchemy.Integer)
        gameStartTime = sqlalchemy.Column(sqlalchemy.BigInteger)
        gameType = sqlalchemy.Column(sqlalchemy.String(30))
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        observers = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.Observer", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.Participant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))


def _sa_bind_all():
    _sa_bind_participant()
    _sa_bind_observer()
    _sa_bind_banned_champion()
    _sa_bind_featured_game_info()
