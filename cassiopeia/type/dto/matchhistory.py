import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.matchhistory import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_match_summary():
    global MatchSummary
    @cassiopeia.type.core.common.inheritdocs
    class MatchSummary(MatchSummary, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryMatch"
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        matchCreation = sqlalchemy.Column(sqlalchemy.BigInteger)
        matchDuration = sqlalchemy.Column(sqlalchemy.Integer)
        matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        matchMode = sqlalchemy.Column(sqlalchemy.String(30))
        matchType = sqlalchemy.Column(sqlalchemy.String(30))
        matchVersion = sqlalchemy.Column(sqlalchemy.String(30))
        participantIdentities = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantIdentity", cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Participant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))
        queueType = sqlalchemy.Column(sqlalchemy.String(30))
        region = sqlalchemy.Column(sqlalchemy.String(30))
        season = sqlalchemy.Column(sqlalchemy.String(30))

def _sa_bind_participant():
    global Participant
    @cassiopeia.type.core.common.inheritdocs
    class Participant(Participant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryParticipant"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        highestAchievedSeasonTier = sqlalchemy.Column(sqlalchemy.String(30))
        masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Mastery", cascade="all, delete-orphan", passive_deletes=True)
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Rune", cascade="all, delete-orphan", passive_deletes=True)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimeline", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryMatch.matchId", ondelete="CASCADE"))

def _sa_bind_participant_identity():
    global ParticipantIdentity
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantIdentity(ParticipantIdentity, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryParticipantIdentity"
        participantId = sqlalchemy.Column(sqlalchemy.Integer)
        player = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Player", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryMatch.matchId", ondelete="CASCADE"))

def _sa_bind_mastery():
    global Mastery
    @cassiopeia.type.core.common.inheritdocs
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryMastery"
        masteryId = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id", ondelete="CASCADE"))

def _sa_bind_participant_stats():
    global ParticipantStats
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantStats(ParticipantStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryParticipantStats"
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
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id", ondelete="CASCADE"))

def _sa_bind_participant_timeline():
    global ParticipantTimeline
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantTimeline(ParticipantTimeline, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryParticipantTimeline"
        ancientGolemAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='ancientGolemAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        ancientGolemKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='ancientGolemKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        assistedLaneDeathsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='assistedLaneDeathsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        assistedLaneKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='assistedLaneKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        baronAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='baronAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        baronKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='baronKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        creepsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='creepsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        csDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='csDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        damageTakenDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='damageTakenDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        damageTakenPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='damageTakenPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        dragonAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='dragonAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        dragonKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='dragonKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        elderLizardAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='elderLizardAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        elderLizardKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='elderLizardKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        goldPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='goldPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inhibitorAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='inhibitorAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inhibitorKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='inhibitorKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        lane = sqlalchemy.Column(sqlalchemy.String(30))
        role = sqlalchemy.Column(sqlalchemy.String(30))
        towerAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        towerKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        towerKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        vilemawAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='vilemawAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        vilemawKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='vilemawKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        wardsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='wardsPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        xpDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='xpDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        xpPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='xpPerMinDeltas')", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id", ondelete="CASCADE"))

def _sa_bind_rune():
    global Rune
    @cassiopeia.type.core.common.inheritdocs
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryRune"
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id", ondelete="CASCADE"))

def _sa_bind_player():
    global Player
    @cassiopeia.type.core.common.inheritdocs
    class Player(Player, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryPlayer"
        matchHistoryUri = sqlalchemy.Column(sqlalchemy.String(50))
        profileIcon = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipantIdentity._id", ondelete="CASCADE"))

def _sa_bind_participant_timeline_data():
    global ParticipantTimelineData
    @cassiopeia.type.core.common.inheritdocs
    class ParticipantTimelineData(ParticipantTimelineData, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "HistoryParticipantTimelineData"
        tenToTwenty = sqlalchemy.Column(sqlalchemy.Float)
        thirtyToEnd = sqlalchemy.Column(sqlalchemy.Float)
        twentyToThirty = sqlalchemy.Column(sqlalchemy.Float)
        zeroToTen = sqlalchemy.Column(sqlalchemy.Float)
        _type = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipantTimeline._id", ondelete="CASCADE"))

def _sa_bind_all():
    _sa_bind_match_summary()
    _sa_bind_participant()
    _sa_bind_participant_identity()
    _sa_bind_mastery()
    _sa_bind_participant_stats()
    _sa_bind_participant_timeline()
    _sa_bind_rune()
    _sa_bind_player()
    _sa_bind_participant_timeline_data()