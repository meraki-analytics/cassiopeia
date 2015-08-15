import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class Rune(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # The count of this rune used by the participant
        self.count = dictionary.get("count", 0)

        # int # The ID of the rune
        self.runeId = dictionary.get("runeId", 0)


class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # The ID of the mastery
        self.masteryId = dictionary.get("masteryId", 0)

        # int # The number of points put into this mastery by the user 
        self.rank = dictionary.get("rank", 0)


class Observer(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # str # Key used to decrypt the spectator grid game data for playback
        self.encryptionKey = dictionary.get("encryptionKey", "")


class CurrentGameParticipant(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # bool # Flag indicating whether or not this participant is a bot
        self.bot = dictionary.get("bot", False)

        # int # The ID of the champion played by this participant
        self.championId = dictionary.get("championId", 0)

        # list<Mastery> # The masteries used by this participant
        self.masteries = [(Mastery(mastery) if not isinstance(mastery, Mastery) else mastery) for mastery in dictionary.get("masteries", []) if mastery]

        # int # The ID of the profile icon used by this participant
        self.profileIconId = dictionary.get("profileIconId", 0)

        # list<Rune> # The runes used by this participant
        self.runes = [(Rune(rune) if not isinstance(rune, Rune) else rune) for rune in dictionary.get("runes", []) if rune]

        # int # The ID of the first summoner spell used by this participant
        self.spell1Id = dictionary.get("spell1Id", 0)

        # int # The ID of the second summoner spell used by this participant
        self.spell2Id = dictionary.get("spell2Id", 0)

        # int # The summoner ID of this participant
        self.summonerId = dictionary.get("summonerId", 0)

        # str # The summoner name of this participant
        self.summonerName = dictionary.get("summonerName", "")

        # int # The team ID of this participant, indicating the participant's team
        self.teamId = dictionary.get("teamId", 0)


class BannedChampion(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # The ID of the banned champion
        self.championId = dictionary.get("championId", 0)

        # int # The turn during which the champion was banned
        self.pickTurn = dictionary.get("pickTurn", 0)

        # int # The ID of the team that banned the champion
        self.teamId = dictionary.get("teamId", 0)


class CurrentGameInfo(cassiopeia.type.dto.common.CassiopeiaDto):
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

        # list<CurrentGameParticipant> # The participant information
        self.participants = [(CurrentGameParticipant(participant) if not isinstance(participant, CurrentGameParticipant) else participant) for participant in dictionary.get("participants", []) if participant]

        # str # The ID of the platform on which the game is being played
        self.platformId = dictionary.get("platformId", "")

    @property
    def champion_ids(self):
        ids = set()
        for ban in self.bannedChampions:
            ids.add(ban.championId)
        for p in self.participants:
            ids.add(p.championId)
        return ids

    @property
    def summoner_ids(self):
        ids = set()
        for p in self.participants:
            if(p.summonerId):
                ids.add(p.summonerId)
        return ids

    @property
    def summoner_spell_ids(self):
        ids = set()
        for p in self.participants:
            if(p.spell1Id):
                ids.add(p.spell1Id)
            if(p.spell2Id):
                ids.add(p.spell2Id)
        return ids

    @property
    def rune_ids(self):
        ids = set()
        for p in self.participants:
            for r in p.runes:
                if(r.runeId):
                    ids.add(r.runeId)
        return ids

    @property
    def mastery_ids(self):
        ids = set()
        for p in self.participants:
            for m in p.masteries:
                if(m.masteryId):
                    ids.add(m.masteryId)
        return ids

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_bind_rune():
    global Rune
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameRune"
        count = sqlalchemy.Column(sqlalchemy.Integer)
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))

def sa_bind_mastery():
    global Mastery
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameMastery"
        masteryId = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))

def sa_bind_observer():
    global Observer
    class Observer(Observer, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameObserver"
        encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))

def sa_bind_current_game_participant():
    global CurrentGameParticipant
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

def sa_bind_banned_champion():
    global BannedChampion
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))

def sa_bind_current_game_info():
    global CurrentGameInfo
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

def sa_bind_all():
    sa_bind_rune()
    sa_bind_mastery()
    sa_bind_observer()
    sa_bind_current_game_participant()
    sa_bind_banned_champion()
    sa_bind_current_game_info()