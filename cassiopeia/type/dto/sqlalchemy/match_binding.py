import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.collections

from cassiopeia.type.dto.match import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_match_detail():
    global MatchDetail
    @cassiopeia.type.core.common.inheritdocs
    class MatchDetail(MatchDetail, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchDetail"
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        matchCreation = sqlalchemy.Column(sqlalchemy.BigInteger)
        matchDuration = sqlalchemy.Column(sqlalchemy.Integer)
        matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        matchMode = sqlalchemy.Column(sqlalchemy.String(30))
        matchType = sqlalchemy.Column(sqlalchemy.String(30))
        matchVersion = sqlalchemy.Column(sqlalchemy.String(30))
        participantIdentities = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantIdentity", cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Participant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))
        queueType = sqlalchemy.Column(sqlalchemy.String(30))
        region = sqlalchemy.Column(sqlalchemy.String(30))
        season = sqlalchemy.Column(sqlalchemy.String(30))
        teams = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Team", cascade="all, delete-orphan", passive_deletes=True)
        timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Timeline", uselist=False, cascade="all, delete-orphan", passive_deletes=True)

def _sa_bind_participant():
    global Participant
    @cassiopeia.type.core.common.inheritdocs
    class Participant(Participant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipant"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        highestAchievedSeasonTier = sqlalchemy.Column(sqlalchemy.String(30))
        masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Mastery", cascade="all, delete-orphan", passive_deletes=True)
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Rune", cascade="all, delete-orphan", passive_deletes=True)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimeline", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))

def _sa_bind_participant_identity():
    global ParticipantIdentity
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantIdentity(ParticipantIdentity, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantIdentity"
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        player = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Player", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))

def _sa_bind_team():
    global Team
    @cassiopeia.type.core.common.inheritdocs
    class Team(Team, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchTeam"
        bans = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
        baronKills = sqlalchemy.Column(sqlalchemy.Integer)
        dominionVictoryScore = sqlalchemy.Column(sqlalchemy.Integer)
        dragonKills = sqlalchemy.Column(sqlalchemy.Integer)
        firstBaron = sqlalchemy.Column(sqlalchemy.Boolean)
        firstBlood = sqlalchemy.Column(sqlalchemy.Boolean)
        firstDragon = sqlalchemy.Column(sqlalchemy.Boolean)
        firstInhibitor = sqlalchemy.Column(sqlalchemy.Boolean)
        firstTower = sqlalchemy.Column(sqlalchemy.Boolean)
        inhibitorKills = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        towerKills = sqlalchemy.Column(sqlalchemy.Integer)
        vilemawKills = sqlalchemy.Column(sqlalchemy.Integer)
        winner = sqlalchemy.Column(sqlalchemy.Boolean)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))

def _sa_bind_timeline():
    global Timeline
    @cassiopeia.type.core.common.inheritdocs
    class Timeline(Timeline, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchTimeline"
        frameInterval = sqlalchemy.Column(sqlalchemy.Integer)
        frames = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Frame", cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchDetail.matchId", ondelete="CASCADE"))

def _sa_bind_mastery():
    global Mastery
    @cassiopeia.type.core.common.inheritdocs
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchMastery"
        masteryId = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))

def _sa_bind_participant_stats():
    global ParticipantStats
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantStats(ParticipantStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantStats"
        assists = sqlalchemy.Column(sqlalchemy.Integer)
        champLevel = sqlalchemy.Column(sqlalchemy.Integer)
        combatPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        deaths = sqlalchemy.Column(sqlalchemy.Integer)
        doubleKills = sqlalchemy.Column(sqlalchemy.Integer)
        firstBloodAssist = sqlalchemy.Column(sqlalchemy.Boolean)
        firstBloodKill = sqlalchemy.Column(sqlalchemy.Boolean)
        firstInhibitorAssist = sqlalchemy.Column(sqlalchemy.Boolean)
        firstInhibitorKill = sqlalchemy.Column(sqlalchemy.Boolean)
        firstTowerAssist = sqlalchemy.Column(sqlalchemy.Boolean)
        firstTowerKill = sqlalchemy.Column(sqlalchemy.Boolean)
        goldEarned = sqlalchemy.Column(sqlalchemy.Integer)
        goldSpent = sqlalchemy.Column(sqlalchemy.Integer)
        inhibitorKills = sqlalchemy.Column(sqlalchemy.Integer)
        item0 = sqlalchemy.Column(sqlalchemy.Integer)
        item1 = sqlalchemy.Column(sqlalchemy.Integer)
        item2 = sqlalchemy.Column(sqlalchemy.Integer)
        item3 = sqlalchemy.Column(sqlalchemy.Integer)
        item4 = sqlalchemy.Column(sqlalchemy.Integer)
        item5 = sqlalchemy.Column(sqlalchemy.Integer)
        item6 = sqlalchemy.Column(sqlalchemy.Integer)
        killingSprees = sqlalchemy.Column(sqlalchemy.Integer)
        kills = sqlalchemy.Column(sqlalchemy.Integer)
        largestCriticalStrike = sqlalchemy.Column(sqlalchemy.Integer)
        largestKillingSpree = sqlalchemy.Column(sqlalchemy.Integer)
        largestMultiKill = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        minionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilledEnemyJungle = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilledTeamJungle = sqlalchemy.Column(sqlalchemy.Integer)
        nodeCapture = sqlalchemy.Column(sqlalchemy.Integer)
        nodeCaptureAssist = sqlalchemy.Column(sqlalchemy.Integer)
        nodeNeutralize = sqlalchemy.Column(sqlalchemy.Integer)
        nodeNeutralizeAssist = sqlalchemy.Column(sqlalchemy.Integer)
        objectivePlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        pentaKills = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        quadraKills = sqlalchemy.Column(sqlalchemy.Integer)
        sightWardsBoughtInGame = sqlalchemy.Column(sqlalchemy.Integer)
        teamObjective = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        totalHeal = sqlalchemy.Column(sqlalchemy.Integer)
        totalPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        totalScoreRank = sqlalchemy.Column(sqlalchemy.Integer)
        totalTimeCrowdControlDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalUnitsHealed = sqlalchemy.Column(sqlalchemy.Integer)
        towerKills = sqlalchemy.Column(sqlalchemy.Integer)
        tripleKills = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        unrealKills = sqlalchemy.Column(sqlalchemy.Integer)
        visionWardsBoughtInGame = sqlalchemy.Column(sqlalchemy.Integer)
        wardsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        wardsPlaced = sqlalchemy.Column(sqlalchemy.Integer)
        winner = sqlalchemy.Column(sqlalchemy.Boolean)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))

def _sa_bind_participant_timeline():
    global ParticipantTimeline
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantTimeline(ParticipantTimeline, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantTimeline"
        ancientGolemAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='ancientGolemAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        ancientGolemKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='ancientGolemKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        assistedLaneDeathsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='assistedLaneDeathsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        assistedLaneKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='assistedLaneKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        baronAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='baronAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        baronKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='baronKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        creepsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='creepsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        csDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='csDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        damageTakenDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='damageTakenDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        damageTakenPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='damageTakenPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        dragonAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='dragonAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        dragonKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='dragonKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        elderLizardAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='elderLizardAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        elderLizardKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='elderLizardKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        goldPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='goldPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inhibitorAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='inhibitorAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inhibitorKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='inhibitorKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        lane = sqlalchemy.Column(sqlalchemy.String(30))
        role = sqlalchemy.Column(sqlalchemy.String(30))
        towerAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='towerAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        towerKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='towerKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        towerKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='towerKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        vilemawAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='vilemawAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        vilemawKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='vilemawKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        wardsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='wardsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        xpDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='xpDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        xpPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.match.ParticipantTimeline._id==cassiopeia.type.dto.match.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.match.ParticipantTimelineData._type=='xpPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))

def _sa_bind_rune():
    global Rune
    @cassiopeia.type.core.common.inheritdocs
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchRune"
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id", ondelete="CASCADE"))

def _sa_bind_player():
    global Player
    @cassiopeia.type.core.common.inheritdocs
    class Player(Player, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchPlayer"
        matchHistoryUri = sqlalchemy.Column(sqlalchemy.String(50))
        profileIcon = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantIdentity._id", ondelete="CASCADE"))

def _sa_bind_banned_champion():
    global BannedChampion
    @cassiopeia.type.core.common.inheritdocs
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchTeam._id", ondelete="CASCADE"))

def _sa_bind_frame():
    global Frame
    @cassiopeia.type.core.common.inheritdocs
    class Frame(Frame, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchFrame"
        events = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Event", cascade="all, delete-orphan", passive_deletes=True)
        participantFrames = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantFrame", collection_class=sqlalchemy.orm.collections.mapped_collection(lambda p: str(p.participantId)), cascade="all, delete-orphan", passive_deletes=True) # OR I HAVE NO IDEA
        timestamp = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchTimeline._id", ondelete="CASCADE"))

def _sa_bind_participant_timeline_data():
    global ParticipantTimelineData
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantTimelineData(ParticipantTimelineData, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantTimelineData"
        tenToTwenty = sqlalchemy.Column(sqlalchemy.Float)
        thirtyToEnd = sqlalchemy.Column(sqlalchemy.Float)
        twentyToThirty = sqlalchemy.Column(sqlalchemy.Float)
        zeroToTen = sqlalchemy.Column(sqlalchemy.Float)
        _type = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantTimeline._id", ondelete="CASCADE"))

def _sa_bind_event():
    global Event
    @cassiopeia.type.core.common.inheritdocs
    class Event(Event, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchEvent"
        ascendedType = sqlalchemy.Column(sqlalchemy.String(30))
        assistingParticipantIds = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        buildingType = sqlalchemy.Column(sqlalchemy.String(30))
        creatorId = sqlalchemy.Column(sqlalchemy.Integer)
        eventType = sqlalchemy.Column(sqlalchemy.String(30))
        itemAfter = sqlalchemy.Column(sqlalchemy.Integer)
        itemBefore = sqlalchemy.Column(sqlalchemy.Integer)
        itemId = sqlalchemy.Column(sqlalchemy.Integer)
        killerId = sqlalchemy.Column(sqlalchemy.Integer)
        laneType = sqlalchemy.Column(sqlalchemy.String(30))
        levelUpType = sqlalchemy.Column(sqlalchemy.String(30))
        monsterType = sqlalchemy.Column(sqlalchemy.String(30))
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        pointCaptured = sqlalchemy.Column(sqlalchemy.String(30))
        position = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Position", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        skillSlot = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        timestamp = sqlalchemy.Column(sqlalchemy.Integer)
        towerType = sqlalchemy.Column(sqlalchemy.String(30))
        victimId = sqlalchemy.Column(sqlalchemy.Integer)
        wardType = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchFrame._id", ondelete="CASCADE"))

def _sa_bind_participant_frame():
    global ParticipantFrame
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantFrame(ParticipantFrame, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchParticipantFrame"
        currentGold = sqlalchemy.Column(sqlalchemy.Integer)
        dominionScore = sqlalchemy.Column(sqlalchemy.Integer)
        jungleMinionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        level = sqlalchemy.Column(sqlalchemy.Integer)
        minionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        position = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Position", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        teamScore = sqlalchemy.Column(sqlalchemy.Integer)
        totalGold = sqlalchemy.Column(sqlalchemy.Integer)
        xp = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchFrame._id", ondelete="CASCADE"))

def _sa_bind_position():
    global Position
    @cassiopeia.type.core.common.inheritdocs
    class Position(Position, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchPosition"
        x = sqlalchemy.Column(sqlalchemy.Integer)
        y = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchEvent._id", ondelete="CASCADE"))
        _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantFrame._id", ondelete="CASCADE"))

def _sa_bind_all():
    _sa_bind_match_detail()
    _sa_bind_participant()
    _sa_bind_participant_identity()
    _sa_bind_team()
    _sa_bind_timeline()
    _sa_bind_mastery()
    _sa_bind_participant_stats()
    _sa_bind_participant_timeline()
    _sa_bind_rune()
    _sa_bind_player()
    _sa_bind_banned_champion()
    _sa_bind_frame()
    _sa_bind_participant_timeline_data()
    _sa_bind_event()
    _sa_bind_participant_frame()
    _sa_bind_position()