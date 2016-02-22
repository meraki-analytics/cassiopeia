import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class Rune(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        count (int): the count of this rune used by the participant
        runeId (int): the ID of the rune
    """
    def __init__(self, dictionary):
        self.count = dictionary.get("count", 0)
        self.runeId = dictionary.get("runeId", 0)


@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        masteryId (int): the ID of the mastery
        rank (int): the number of points put into this mastery by the user
    """
    def __init__(self, dictionary):
        self.masteryId = dictionary.get("masteryId", 0)
        self.rank = dictionary.get("rank", 0)


@cassiopeia.type.core.common.inheritdocs
class Observer(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        encryptionKey (str): key used to decrypt the spectator grid game data for playback
    """
    def __init__(self, dictionary):
        self.encryptionKey = dictionary.get("encryptionKey", "")


@cassiopeia.type.core.common.inheritdocs
class CurrentGameParticipant(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        bot (bool): flag indicating whether or not this participant is a bot
        championId (int): the ID of the champion played by this participant
        masteries (list<Mastery>): the masteries used by this participant
        profileIconId (int): the ID of the profile icon used by this participant
        runes (list<Rune>): the runes used by this participant
        spell1Id (int): the ID of the first summoner spell used by this participant
        spell2Id (int): the ID of the second summoner spell used by this participant
        summonerId (int): the summoner ID of this participant
        summonerName (str): the summoner name of this participant
        teamId (int): the team ID of this participant, indicating the participant's team
    """
    def __init__(self, dictionary):
        self.bot = dictionary.get("bot", False)
        self.championId = dictionary.get("championId", 0)
        self.masteries = [(Mastery(mastery) if not isinstance(mastery, Mastery) else mastery) for mastery in dictionary.get("masteries", []) if mastery]
        self.profileIconId = dictionary.get("profileIconId", 0)
        self.runes = [(Rune(rune) if not isinstance(rune, Rune) else rune) for rune in dictionary.get("runes", []) if rune]
        self.spell1Id = dictionary.get("spell1Id", 0)
        self.spell2Id = dictionary.get("spell2Id", 0)
        self.summonerId = dictionary.get("summonerId", 0)
        self.summonerName = dictionary.get("summonerName", "")
        self.teamId = dictionary.get("teamId", 0)


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
class CurrentGameInfo(cassiopeia.type.dto.common.CassiopeiaDto):
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
        participants (list<CurrentGameParticipant>): the participant information
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
        self.participants = [(CurrentGameParticipant(participant) if not isinstance(participant, CurrentGameParticipant) else participant) for participant in dictionary.get("participants", []) if participant]
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
    def summoner_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for p in self.participants:
            if p.summonerId:
                ids.add(p.summonerId)
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

    @property
    def rune_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for p in self.participants:
            for r in p.runes:
                if r.runeId:
                    ids.add(r.runeId)
        return ids

    @property
    def mastery_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for p in self.participants:
            for m in p.masteries:
                if m.masteryId:
                    ids.add(m.masteryId)
        return ids


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_rune():
    global Rune

    @cassiopeia.type.core.common.inheritdocs
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameRune"
        count = sqlalchemy.Column(sqlalchemy.Integer)
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))


def _sa_bind_mastery():
    global Mastery

    @cassiopeia.type.core.common.inheritdocs
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameMastery"
        masteryId = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))


def _sa_bind_observer():
    global Observer

    @cassiopeia.type.core.common.inheritdocs
    class Observer(Observer, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameObserver"
        encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_current_game_participant():
    global CurrentGameParticipant

    @cassiopeia.type.core.common.inheritdocs
    class CurrentGameParticipant(CurrentGameParticipant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameParticipant"
        bot = sqlalchemy.Column(sqlalchemy.Boolean)
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Mastery", cascade="all, delete-orphan", passive_deletes=True)
        profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Rune", cascade="all, delete-orphan", passive_deletes=True)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_banned_champion():
    global BannedChampion

    @cassiopeia.type.core.common.inheritdocs
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))


def _sa_bind_current_game_info():
    global CurrentGameInfo

    @cassiopeia.type.core.common.inheritdocs
    class CurrentGameInfo(CurrentGameInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameInfo"
        bannedChampions = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
        gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        gameLength = sqlalchemy.Column(sqlalchemy.Integer)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        gameQueueConfigId = sqlalchemy.Column(sqlalchemy.Integer)
        gameStartTime = sqlalchemy.Column(sqlalchemy.BigInteger)
        gameType = sqlalchemy.Column(sqlalchemy.String(30))
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        observers = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Observer", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.CurrentGameParticipant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))


def _sa_bind_all():
    _sa_bind_rune()
    _sa_bind_mastery()
    _sa_bind_observer()
    _sa_bind_current_game_participant()
    _sa_bind_banned_champion()
    _sa_bind_current_game_info()
