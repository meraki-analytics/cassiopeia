import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class PlayerHistory(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<MatchSummary> # List of matches for the player
        self.matches = [(MatchSummary(match) if not isinstance(match, MatchSummary) else match) for match in dictionary.get("matches", []) if match]

    @property
    def champion_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.champion_ids
        return ids

    @property
    def item_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.item_ids
        return ids

    @property
    def mastery_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.mastery_ids
        return ids

    @property
    def rune_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.rune_ids
        return ids

    @property
    def summoner_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.summoner_ids
        return ids

    @property
    def summoner_spell_ids(self):
        ids = set()
        for m in self.matches:
            ids = ids | m.summoner_spell_ids
        return ids


class MatchSummary(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryMatch"
    mapId = sqlalchemy.Column(sqlalchemy.Integer)
    matchCreation = sqlalchemy.Column(sqlalchemy.BigInteger)
    matchDuration = sqlalchemy.Column(sqlalchemy.Integer)
    matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    matchMode = sqlalchemy.Column(sqlalchemy.String(30))
    matchType = sqlalchemy.Column(sqlalchemy.String(30))
    matchVersion = sqlalchemy.Column(sqlalchemy.String(30))
    participantIdentities = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantIdentity", cascade="all, delete-orphan, merge", passive_deletes=True)
    participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Participant", cascade="all, delete-orphan, merge", passive_deletes=True)
    platformId = sqlalchemy.Column(sqlalchemy.String(30))
    queueType = sqlalchemy.Column(sqlalchemy.String(30))
    region = sqlalchemy.Column(sqlalchemy.String(30))
    season = sqlalchemy.Column(sqlalchemy.String(30))

    def __init__(self, dictionary):
        # int # Match map ID
        self.mapId = dictionary.get("mapId", 0)

        # int # Match creation time. Designates when the team select lobby is created and/or the match is made through match making, not when the game actually starts.
        self.matchCreation = dictionary.get("matchCreation", 0)

        # int # Match duration
        self.matchDuration = dictionary.get("matchDuration", 0)

        # int # ID of the match
        self.matchId = dictionary.get("matchId", 0)

        # str # Match mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.matchMode = dictionary.get("matchMode", "")

        # str # Match type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.matchType = dictionary.get("matchType", "")

        # str # Match version
        self.matchVersion = dictionary.get("matchVersion", "")

        # list<ParticipantIdentity> # Participant identity information
        self.participantIdentities = [(ParticipantIdentity(pi) if not isinstance(pi, ParticipantIdentity) else pi) for pi in dictionary.get("participantIdentities", []) if pi]

        # list<Participant> # Participant information
        self.participants = [(Participant(p) if not isinstance(p, Participant) else p) for p in dictionary.get("participants", []) if p]

        # str # Platform ID of the match
        self.platformId = dictionary.get("platformId", "")

        # str # Match queue type (Legal values: CUSTOM, NORMAL_5x5_BLIND, RANKED_SOLO_5x5, RANKED_PREMADE_5x5, BOT_5x5, NORMAL_3x3, RANKED_PREMADE_3x3, NORMAL_5x5_DRAFT, ODIN_5x5_BLIND, ODIN_5x5_DRAFT, BOT_ODIN_5x5, BOT_5x5_INTRO, BOT_5x5_BEGINNER, BOT_5x5_INTERMEDIATE, RANKED_TEAM_3x3, RANKED_TEAM_5x5, BOT_TT_3x3, GROUP_FINDER_5x5, ARAM_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF_5x5, ONEFORALL_MIRRORMODE_5x5, BOT_URF_5x5, NIGHTMARE_BOT_5x5_RANK1, NIGHTMARE_BOT_5x5_RANK2, NIGHTMARE_BOT_5x5_RANK5, ASCENSION_5x5, HEXAKILL, KING_PORO_5x5, COUNTER_PICK)
        self.queueType = dictionary.get("queueType", "")

        # str # Region where the match was played
        self.region = dictionary.get("region", "")

        # str # Season match was played (Legal values: PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015)
        self.season = dictionary.get("season", "")

    @property
    def item_ids(self):
        ids = set()
        for p in self.participants:
            s = p.stats
            if(s.item0):
                ids.add(s.item0)
            if(s.item1):
                ids.add(s.item1)
            if(s.item2):
                ids.add(s.item2)
            if(s.item3):
                ids.add(s.item3)
            if(s.item4):
                ids.add(s.item4)
            if(s.item5):
                ids.add(s.item5)
            if(s.item6):
                ids.add(s.item6)
        return ids

    @property
    def champion_ids(self):
        ids = set()
        for p in self.participants:
            if(p.championId):
                ids.add(p.championId)
        return ids

    @property
    def mastery_ids(self):
        ids = set()
        for p in self.participants:
            for m in p.masteries:
                if(m.masteryId):
                    ids.add(m.masteryId)
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
    def summoner_ids(self):
        ids = set()
        for p in self.participantIdentities:
            if(p.player and p.player.summonerId):
                ids.add(p.player.summonerId)
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


class Participant(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryParticipant"
    championId = sqlalchemy.Column(sqlalchemy.Integer)
    highestAchievedSeasonTier = sqlalchemy.Column(sqlalchemy.String(30))
    masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Mastery", cascade="all, delete-orphan, merge", passive_deletes=True)
    participantId = sqlalchemy.Column(sqlalchemy.Integer)
    runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Rune", cascade="all, delete-orphan, merge", passive_deletes=True)
    spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
    spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
    stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantStats", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    teamId = sqlalchemy.Column(sqlalchemy.Integer)
    timeline = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimeline", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryMatch.matchId"))

    def __init__(self, dictionary):
        # int # Champion ID
        self.championId = dictionary.get("championId", 0)

        # str # Highest ranked tier achieved for the previous season, if any, otherwise null. Used to display border in game loading screen. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, UNRANKED)
        self.highestAchievedSeasonTier = dictionary.get("highestAchievedSeasonTier", "")

        # list<Mastery> # List of mastery information
        self.masteries = [(Mastery(m) if not isinstance(m, Mastery) else m) for m in dictionary.get("masteries", []) if m]

        # int # Participant ID
        self.participantId = dictionary.get("participantId", 0)

        # list<Rune> # List of rune information
        self.runes = [(Rune(r) if not isinstance(r, Rune) else r) for r in dictionary.get("runes", []) if r]

        # int # First summoner spell ID
        self.spell1Id = dictionary.get("spell1Id", 0)

        # int # Second summoner spell ID
        self.spell2Id = dictionary.get("spell2Id", 0)

        # ParticipantStats # Participant statistics
        val = dictionary.get("stats", None)
        self.stats = ParticipantStats(val) if val and not isinstance(val, ParticipantStats) else val

        # int # Team ID
        self.teamId = dictionary.get("teamId", 0)

        # ParticipantTimeline # Timeline data. Delta fields refer to values for the specified period (e.g., the gold per minute over the first 10 minutes of the game versus the second 20 minutes of the game. Diffs fields refer to the deltas versus the calculated lane opponent(s).
        val = dictionary.get("timeline", None)
        self.timeline = ParticipantTimeline(val) if val and not isinstance(val, ParticipantTimeline) else val


class ParticipantIdentity(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryParticipantIdentity"
    participantId = sqlalchemy.Column(sqlalchemy.Integer)
    player = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.Player", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryMatch.matchId"))

    def __init__(self, dictionary):
        # int # Participant ID
        self.participantId = dictionary.get("participantId", 0)

        # Player # Player information
        val = dictionary.get("player", None)
        self.player = Player(val) if val and not isinstance(val, Player) else val


class Mastery(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryMastery"
    masteryId = sqlalchemy.Column(sqlalchemy.Integer)
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id"))

    def __init__(self, dictionary):
        # int # Mastery ID
        self.masteryId = dictionary.get("masteryId", 0)

        # int # Mastery rank
        self.rank = dictionary.get("rank", 0)


class ParticipantStats(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id"))

    def __init__(self, dictionary):
        # int # Number of assists
        self.assists = dictionary.get("assists", 0)

        # int # Champion level achieved
        self.champLevel = dictionary.get("champLevel", 0)

        # int # If game was a dominion game, player's combat score, otherwise 0
        self.combatPlayerScore = dictionary.get("combatPlayerScore", 0)

        # int # Number of deaths
        self.deaths = dictionary.get("deaths", 0)

        # int # Number of double kills
        self.doubleKills = dictionary.get("doubleKills", 0)

        # bool # Flag indicating if participant got an assist on first blood
        self.firstBloodAssist = dictionary.get("firstBloodAssist", False)

        # bool # Flag indicating if participant got first blood
        self.firstBloodKill = dictionary.get("firstBloodKill", False)

        # bool # Flag indicating if participant got an assist on the first inhibitor
        self.firstInhibitorAssist = dictionary.get("firstInhibitorAssist", False)

        # bool # Flag indicating if participant destroyed the first inhibitor
        self.firstInhibitorKill = dictionary.get("firstInhibitorKill", False)

        # bool # Flag indicating if participant got an assist on the first tower
        self.firstTowerAssist = dictionary.get("firstTowerAssist", False)

        # bool # Flag indicating if participant destroyed the first tower
        self.firstTowerKill = dictionary.get("firstTowerKill", False)

        # int # Gold earned
        self.goldEarned = dictionary.get("goldEarned", 0)

        # int # Gold spent
        self.goldSpent = dictionary.get("goldSpent", 0)

        # int # Number of inhibitor kills
        self.inhibitorKills = dictionary.get("inhibitorKills", 0)

        # int # First item ID
        self.item0 = dictionary.get("item0", 0)

        # int # Second item ID
        self.item1 = dictionary.get("item1", 0)

        # int # Third item ID
        self.item2 = dictionary.get("item2", 0)

        # int # Fourth item ID
        self.item3 = dictionary.get("item3", 0)

        # int # Fifth item ID
        self.item4 = dictionary.get("item4", 0)

        # int # Sixth item ID
        self.item5 = dictionary.get("item5", 0)

        # int # Seventh item ID
        self.item6 = dictionary.get("item6", 0)

        # int # Number of killing sprees
        self.killingSprees = dictionary.get("killingSprees", 0)

        # int # Number of kills
        self.kills = dictionary.get("kills", 0)

        # int # Largest critical strike
        self.largestCriticalStrike = dictionary.get("largestCriticalStrike", 0)

        # int # Largest killing spree
        self.largestKillingSpree = dictionary.get("largestKillingSpree", 0)

        # int # Largest multi kill
        self.largestMultiKill = dictionary.get("largestMultiKill", 0)

        # int # Magical damage dealt
        self.magicDamageDealt = dictionary.get("magicDamageDealt", 0)

        # int # Magical damage dealt to champions
        self.magicDamageDealtToChampions = dictionary.get("magicDamageDealtToChampions", 0)

        # int # Magic damage taken
        self.magicDamageTaken = dictionary.get("magicDamageTaken", 0)

        # int # Minions killed
        self.minionsKilled = dictionary.get("minionsKilled", 0)

        # int # Neutral minions killed
        self.neutralMinionsKilled = dictionary.get("neutralMinionsKilled", 0)

        # int # Neutral jungle minions killed in the enemy team's jungle
        self.neutralMinionsKilledEnemyJungle = dictionary.get("neutralMinionsKilledEnemyJungle", 0)

        # int # Neutral jungle minions killed in your team's jungle
        self.neutralMinionsKilledTeamJungle = dictionary.get("neutralMinionsKilledTeamJungle", 0)

        # int # If game was a dominion game, number of node captures
        self.nodeCapture = dictionary.get("nodeCapture", 0)

        # int # If game was a dominion game, number of node capture assists
        self.nodeCaptureAssist = dictionary.get("nodeCaptureAssist", 0)

        # int # If game was a dominion game, number of node neutralizations
        self.nodeNeutralize = dictionary.get("nodeNeutralize", 0)

        # int # If game was a dominion game, number of node neutralization assists
        self.nodeNeutralizeAssist = dictionary.get("nodeNeutralizeAssist", 0)

        # int # If game was a dominion game, player's objectives score, otherwise 0
        self.objectivePlayerScore = dictionary.get("objectivePlayerScore", 0)

        # int # Number of penta kills
        self.pentaKills = dictionary.get("pentaKills", 0)

        # int # Physical damage dealt
        self.physicalDamageDealt = dictionary.get("physicalDamageDealt", 0)

        # int # Physical damage dealt to champions
        self.physicalDamageDealtToChampions = dictionary.get("physicalDamageDealtToChampions", 0)

        # int # Physical damage taken
        self.physicalDamageTaken = dictionary.get("physicalDamageTaken", 0)

        # int # Number of quadra kills
        self.quadraKills = dictionary.get("quadraKills", 0)

        # int # Sight wards purchased
        self.sightWardsBoughtInGame = dictionary.get("sightWardsBoughtInGame", 0)

        # int # If game was a dominion game, number of completed team objectives (i.e., quests)
        self.teamObjective = dictionary.get("teamObjective", 0)

        # int # Total damage dealt
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)

        # int # Total damage dealt to champions
        self.totalDamageDealtToChampions = dictionary.get("totalDamageDealtToChampions", 0)

        # int # Total damage taken
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)

        # int # Total heal amount
        self.totalHeal = dictionary.get("totalHeal", 0)

        # int # If game was a dominion game, player's total score, otherwise 0
        self.totalPlayerScore = dictionary.get("totalPlayerScore", 0)

        # int # If game was a dominion game, team rank of the player's total score (e.g., 1-5)
        self.totalScoreRank = dictionary.get("totalScoreRank", 0)

        # int # Total dealt crowd control time
        self.totalTimeCrowdControlDealt = dictionary.get("totalTimeCrowdControlDealt", 0)

        # int # Total units healed
        self.totalUnitsHealed = dictionary.get("totalUnitsHealed", 0)

        # int # Number of tower kills
        self.towerKills = dictionary.get("towerKills", 0)

        # int # Number of triple kills
        self.tripleKills = dictionary.get("tripleKills", 0)

        # int # True damage dealt
        self.trueDamageDealt = dictionary.get("trueDamageDealt", 0)

        # int # True damage dealt to champions
        self.trueDamageDealtToChampions = dictionary.get("trueDamageDealtToChampions", 0)

        # int # True damage taken
        self.trueDamageTaken = dictionary.get("trueDamageTaken", 0)

        # int # Number of unreal kills
        self.unrealKills = dictionary.get("unrealKills", 0)

        # int # Vision wards purchased
        self.visionWardsBoughtInGame = dictionary.get("visionWardsBoughtInGame", 0)

        # int # Number of wards killed
        self.wardsKilled = dictionary.get("wardsKilled", 0)

        # int # Number of wards placed
        self.wardsPlaced = dictionary.get("wardsPlaced", 0)

        # bool # Flag indicating whether or not the participant won
        self.winner = dictionary.get("winner", False)


class ParticipantTimeline(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryParticipantTimeline"
    ancientGolemAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='ancientGolemAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    ancientGolemKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='ancientGolemKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    assistedLaneDeathsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='assistedLaneDeathsPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    assistedLaneKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='assistedLaneKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    baronAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='baronAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    baronKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='baronKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    creepsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='creepsPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    csDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='csDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    damageTakenDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='damageTakenDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    damageTakenPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='damageTakenPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    dragonAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='dragonAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    dragonKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='dragonKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    elderLizardAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='elderLizardAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    elderLizardKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='elderLizardKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    goldPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='goldPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    inhibitorAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='inhibitorAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    inhibitorKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='inhibitorKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    lane = sqlalchemy.Column(sqlalchemy.String(30))
    role = sqlalchemy.Column(sqlalchemy.String(30))
    towerAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    towerKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    towerKillsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='towerKillsPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    vilemawAssistsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='vilemawAssistsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    vilemawKillsPerMinCounts = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='vilemawKillsPerMinCounts')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    wardsPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='wardsPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    xpDiffPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='xpDiffPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    xpPerMinDeltas = sqlalchemy.orm.relationship("cassiopeia.type.dto.matchhistory.ParticipantTimelineData", primaryjoin="and_(cassiopeia.type.dto.matchhistory.ParticipantTimeline._id==cassiopeia.type.dto.matchhistory.ParticipantTimelineData._timeline_id, cassiopeia.type.dto.matchhistory.ParticipantTimelineData._type=='xpPerMinDeltas')", uselist=False, cascade="all, delete-orphan, merge", passive_deletes=True)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id"))

    def __init__(self, dictionary):
        # ParticipantTimelineData # Ancient golem assists per minute timeline counts
        val = dictionary.get("ancientGolemAssistsPerMinCounts", None)
        self.ancientGolemAssistsPerMinCounts = ParticipantTimelineData(val, "ancientGolemAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Ancient golem kills per minute timeline counts
        val = dictionary.get("ancientGolemKillsPerMinCounts", None)
        self.ancientGolemKillsPerMinCounts = ParticipantTimelineData(val, "ancientGolemKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Assisted lane deaths per minute timeline data
        val = dictionary.get("assistedLaneDeathsPerMinDeltas", None)
        self.assistedLaneDeathsPerMinDeltas = ParticipantTimelineData(val, "assistedLaneDeathsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Assisted lane kills per minute timeline data
        val = dictionary.get("assistedLaneKillsPerMinDeltas", None)
        self.assistedLaneKillsPerMinDeltas = ParticipantTimelineData(val, "assistedLaneKillsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Baron assists per minute timeline counts
        val = dictionary.get("baronAssistsPerMinCounts", None)
        self.baronAssistsPerMinCounts = ParticipantTimelineData(val, "baronAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Baron kills per minute timeline counts
        val = dictionary.get("baronKillsPerMinCounts", None)
        self.baronKillsPerMinCounts = ParticipantTimelineData(val, "baronKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Creeps per minute timeline data
        val = dictionary.get("creepsPerMinDeltas", None)
        self.creepsPerMinDeltas = ParticipantTimelineData(val, "creepsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Creep score difference per minute timeline data
        val = dictionary.get("csDiffPerMinDeltas", None)
        self.csDiffPerMinDeltas = ParticipantTimelineData(val, "csDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Damage taken difference per minute timeline data
        val = dictionary.get("damageTakenDiffPerMinDeltas", None)
        self.damageTakenDiffPerMinDeltas = ParticipantTimelineData(val, "damageTakenDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Damage taken per minute timeline data
        val = dictionary.get("damageTakenPerMinDeltas", None)
        self.damageTakenPerMinDeltas = ParticipantTimelineData(val, "damageTakenPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Dragon assists per minute timeline counts
        val = dictionary.get("dragonAssistsPerMinCounts", None)
        self.dragonAssistsPerMinCounts = ParticipantTimelineData(val, "dragonAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Dragon kills per minute timeline counts
        val = dictionary.get("dragonKillsPerMinCounts", None)
        self.dragonKillsPerMinCounts = ParticipantTimelineData(val, "dragonKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Elder lizard assists per minute timeline counts
        val = dictionary.get("elderLizardAssistsPerMinCounts", None)
        self.elderLizardAssistsPerMinCounts = ParticipantTimelineData(val, "elderLizardAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Elder lizard kills per minute timeline counts
        val = dictionary.get("elderLizardKillsPerMinCounts", None)
        self.elderLizardKillsPerMinCounts = ParticipantTimelineData(val, "elderLizardKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Gold per minute timeline data
        val = dictionary.get("goldPerMinDeltas", None)
        self.goldPerMinDeltas = ParticipantTimelineData(val, "goldPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Inhibitor assists per minute timeline counts
        val = dictionary.get("inhibitorAssistsPerMinCounts", None)
        self.inhibitorAssistsPerMinCounts = ParticipantTimelineData(val, "inhibitorAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Inhibitor kills per minute timeline counts
        val = dictionary.get("inhibitorKillsPerMinCounts", None)
        self.inhibitorKillsPerMinCounts = ParticipantTimelineData(val, "inhibitorKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # str # Participant's lane (Legal values: MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM)
        self.lane = dictionary.get("lane", "")

        # str # Participant's role (Legal values: DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT)
        self.role = dictionary.get("role", "")

        # ParticipantTimelineData # Tower assists per minute timeline counts
        val = dictionary.get("towerAssistsPerMinCounts", None)
        self.towerAssistsPerMinCounts = ParticipantTimelineData(val, "towerAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Tower kills per minute timeline counts
        val = dictionary.get("towerKillsPerMinCounts", None)
        self.towerKillsPerMinCounts = ParticipantTimelineData(val, "towerKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Tower kills per minute timeline data
        val = dictionary.get("towerKillsPerMinDeltas", None)
        self.towerKillsPerMinDeltas = ParticipantTimelineData(val, "towerKillsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Vilemaw assists per minute timeline counts
        val = dictionary.get("vilemawAssistsPerMinCounts", None)
        self.vilemawAssistsPerMinCounts = ParticipantTimelineData(val, "vilemawAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Vilemaw kills per minute timeline counts
        val = dictionary.get("vilemawKillsPerMinCounts", None)
        self.vilemawKillsPerMinCounts = ParticipantTimelineData(val, "vilemawKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Wards placed per minute timeline data
        val = dictionary.get("wardsPerMinDeltas", None)
        self.wardsPerMinDeltas = ParticipantTimelineData(val, "wardsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Experience difference per minute timeline data
        val = dictionary.get("xpDiffPerMinDeltas", None)
        self.xpDiffPerMinDeltas = ParticipantTimelineData(val, "xpDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Experience per minute timeline data
        val = dictionary.get("xpPerMinDeltas", None)
        self.xpPerMinDeltas = ParticipantTimelineData(val, "xpPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val


class Rune(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryRune"
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    runeId = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipant._id"))

    def __init__(self, dictionary):
        # int # Rune rank
        self.rank = dictionary.get("rank", 0)

        # int # Rune ID
        self.runeId = dictionary.get("runeId", 0)


class Player(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryPlayer"
    matchHistoryUri = sqlalchemy.Column(sqlalchemy.String(50))
    profileIcon = sqlalchemy.Column(sqlalchemy.Integer)
    summonerId = sqlalchemy.Column(sqlalchemy.Integer)
    summonerName = sqlalchemy.Column(sqlalchemy.String(30))
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipantIdentity._id"))

    def __init__(self, dictionary):
        # str # Match history URI
        self.matchHistoryUri = dictionary.get("matchHistoryUri", "")

        # int # Profile icon ID
        self.profileIcon = dictionary.get("profileIcon", 0)

        # int # Summoner ID
        self.summonerId = dictionary.get("summonerId", 0)

        # str # Summoner name
        self.summonerName = dictionary.get("summonerName", "")


class ParticipantTimelineData(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HistoryParticipantTimelineData"
    tenToTwenty = sqlalchemy.Column(sqlalchemy.Float)
    thirtyToEnd = sqlalchemy.Column(sqlalchemy.Float)
    twentyToThirty = sqlalchemy.Column(sqlalchemy.Float)
    zeroToTen = sqlalchemy.Column(sqlalchemy.Float)
    _type = sqlalchemy.Column(sqlalchemy.String(50))
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("HistoryParticipantTimeline._id"))

    def __init__(self, dictionary, type_=None):
        # float # Value per minute from 10 min to 20 min
        self.tenToTwenty = dictionary.get("tenToTwenty", 0.0)

        # float # Value per minute from 30 min to the end of the game
        self.thirtyToEnd = dictionary.get("thirtyToEnd", 0.0)

        # float # Value per minute from 20 min to 30 min
        self.twentyToThirty = dictionary.get("twentyToThirty", 0.0)

        # float # Value per minute from the beginning of the game to 10 min
        self.zeroToTen = dictionary.get("zeroToTen", 0.0)

        self._type = type_