import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.collections

import cassiopeia.type.dto.common

class MatchDetail(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "Match"
    mapId = sqlalchemy.Column(sqlalchemy.Integer)
    matchCreation = sqlalchemy.Column(sqlalchemy.Integer)
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

        # list<Team> # Team information
        self.teams = [(Team(t) if not isinstance(t, Team) else t) for t in dictionary.get("teams", []) if t]

        # Timeline # Match timeline data (not included by default)
        val = dictionary.get("timeline", None)
        self.timeline = Timeline(val) if val and not isinstance(val, Timeline) else val

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
        for t in self.teams:
            for b in t.bans:
                if(b.championId):
                    ids.add(b.championId)
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
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Match.matchId"))

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
    __tablename__ = "MatchParticipantIdentity"
    participantId = sqlalchemy.Column(sqlalchemy.Integer)
    player = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Player", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Match.matchId"))

    def __init__(self, dictionary):
        # int # Participant ID
        self.participantId = dictionary.get("participantId", 0)

        # Player # Player information
        val = dictionary.get("player", None)
        self.player = Player(val) if val and not isinstance(val, Player) else val


class Team(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Match.matchId"))

    def __init__(self, dictionary):
        # list<BannedChampion> # If game was draft mode, contains banned champion data, otherwise null
        self.bans = [(BannedChampion(c) if not isinstance(c, BannedChampion) else c) for c in dictionary.get("bans", []) if c]

        # int # Number of times the team killed baron
        self.baronKills = dictionary.get("baronKills", 0)

        # int # If game was a dominion game, specifies the points the team had at game end, otherwise null
        self.dominionVictoryScore = dictionary.get("dominionVictoryScore", 0)

        # int # Number of times the team killed dragon
        self.dragonKills = dictionary.get("dragonKills", 0)

        # bool # Flag indicating whether or not the team got the first baron kill
        self.firstBaron = dictionary.get("firstBaron", False)

        # bool # Flag indicating whether or not the team got first blood
        self.firstBlood = dictionary.get("firstBlood", False)

        # bool # Flag indicating whether or not the team got the first dragon kill
        self.firstDragon = dictionary.get("firstDragon", False)

        # bool # Flag indicating whether or not the team destroyed the first inhibitor
        self.firstInhibitor = dictionary.get("firstInhibitor", False)

        # bool # Flag indicating whether or not the team destroyed the first tower
        self.firstTower = dictionary.get("firstTower", False)

        # int # Number of inhibitors the team destroyed
        self.inhibitorKills = dictionary.get("inhibitorKills", 0)

        # int # Team ID
        self.teamId = dictionary.get("teamId", 0)

        # int # Number of towers the team destroyed
        self.towerKills = dictionary.get("towerKills", 0)

        # int # Number of times the team killed vilemaw
        self.vilemawKills = dictionary.get("vilemawKills", 0)

        # bool # Flag indicating whether or not the team won
        self.winner = dictionary.get("winner", False)


class Timeline(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchTimeline"
    frameInterval = sqlalchemy.Column(sqlalchemy.Integer)
    frames = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Frame", cascade="all, delete-orphan", passive_deletes=True)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _match_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Match.matchId"))

    def __init__(self, dictionary):
        # int # Time between each returned frame in milliseconds.
        self.frameInterval = dictionary.get("frameInterval", 0)

        # list<Frame> # List of timeline frames for the game.
        self.frames = [(Frame(f) if not isinstance(f, Frame) else f) for f in dictionary.get("frames", []) if f]


class Mastery(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchMastery"
    masteryId = sqlalchemy.Column(sqlalchemy.Integer)
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id"))

    def __init__(self, dictionary):
        # int # Mastery ID
        self.masteryId = dictionary.get("masteryId", 0)

        # int # Mastery rank
        self.rank = dictionary.get("rank", 0)


class ParticipantStats(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id"))

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
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id"))

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
    __tablename__ = "MatchRune"
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    runeId = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipant._id"))

    def __init__(self, dictionary):
        # int # Rune rank
        self.rank = dictionary.get("rank", 0)

        # int # Rune ID
        self.runeId = dictionary.get("runeId", 0)


class Player(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchPlayer"
    matchHistoryUri = sqlalchemy.Column(sqlalchemy.String(50))
    profileIcon = sqlalchemy.Column(sqlalchemy.Integer)
    summonerId = sqlalchemy.Column(sqlalchemy.Integer)
    summonerName = sqlalchemy.Column(sqlalchemy.String(30))
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantIdentity._id"))

    def __init__(self, dictionary):
        # str # Match history URI
        self.matchHistoryUri = dictionary.get("matchHistoryUri", "")

        # int # Profile icon ID
        self.profileIcon = dictionary.get("profileIcon", 0)

        # int # Summoner ID
        self.summonerId = dictionary.get("summonerId", 0)

        # str # Summoner name
        self.summonerName = dictionary.get("summonerName", "")


class BannedChampion(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchBannedChampion"
    championId = sqlalchemy.Column(sqlalchemy.Integer)
    pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchTeam._id"))

    def __init__(self, dictionary):
        # int # Banned champion ID
        self.championId = dictionary.get("championId", 0)

        # int # Turn during which the champion was banned
        self.pickTurn = dictionary.get("pickTurn", 0)


class Frame(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchFrame"
    events = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.Event", cascade="all, delete-orphan", passive_deletes=True)
    participantFrames = sqlalchemy.orm.relationship("cassiopeia.type.dto.match.ParticipantFrame", collection_class=sqlalchemy.orm.collections.mapped_collection(lambda p: str(p.participantId)), cascade="all, delete-orphan", passive_deletes=True) # OR I HAVE NO IDEA
    timestamp = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchTimeline._id"))

    def __init__(self, dictionary):
        # list<Event> # List of events for this frame.
        self.events = [(Event(e) if not isinstance(e, Event) else e) for e in dictionary.get("events", []) if e]

        # dict<str, ParticipantFrame> # Map of each participant ID to the participant's information for the frame.
        self.participantFrames = {i: ParticipantFrame(pf) if not isinstance(pf, ParticipantFrame) else pf for i, pf in dictionary.get("participantFrames", {}).items()}

        # int # Represents how many milliseconds into the game the frame occurred.
        self.timestamp = dictionary.get("timestamp", 0)


class ParticipantTimelineData(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchParticipantTimelineData"
    tenToTwenty = sqlalchemy.Column(sqlalchemy.Float)
    thirtyToEnd = sqlalchemy.Column(sqlalchemy.Float)
    twentyToThirty = sqlalchemy.Column(sqlalchemy.Float)
    zeroToTen = sqlalchemy.Column(sqlalchemy.Float)
    _type = sqlalchemy.Column(sqlalchemy.String(50))
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _timeline_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantTimeline._id"))

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


class Event(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchFrame._id"))

    def __init__(self, dictionary):
        # str # The ascended type of the event. Only present if relevant. Note that CLEAR_ASCENDED refers to when a participants kills the ascended player. (Legal values: CHAMPION_ASCENDED, CLEAR_ASCENDED, MINION_ASCENDED)
        self.ascendedType = dictionary.get("ascendedType", "")

        # list<int> # The assisting participant IDs of the event. Only present if relevant.
        self.assistingParticipantIds = dictionary.get("assistingParticipantIds", [])

        # str # The building type of the event. Only present if relevant. (Legal values: INHIBITOR_BUILDING, TOWER_BUILDING)
        self.buildingType = dictionary.get("buildingType", "")

        # int # The creator ID of the event. Only present if relevant.
        self.creatorId = dictionary.get("creatorId", 0)

        # str # Event type. (Legal values: ASCENDED_EVENT, BUILDING_KILL, CAPTURE_POINT, CHAMPION_KILL, ELITE_MONSTER_KILL, ITEM_DESTROYED, ITEM_PURCHASED, ITEM_SOLD, ITEM_UNDO, PORO_KING_SUMMON, SKILL_LEVEL_UP, WARD_KILL, WARD_PLACED)
        self.eventType = dictionary.get("eventType", "")

        # int # The ending item ID of the event. Only present if relevant.
        self.itemAfter = dictionary.get("itemAfter", 0)

        # int # The starting item ID of the event. Only present if relevant.
        self.itemBefore = dictionary.get("itemBefore", 0)

        # int # The item ID of the event. Only present if relevant.
        self.itemId = dictionary.get("itemId", 0)

        # int # The killer ID of the event. Only present if relevant. Killer ID 0 indicates a minion.
        self.killerId = dictionary.get("killerId", 0)

        # str # The lane type of the event. Only present if relevant. (Legal values: BOT_LANE, MID_LANE, TOP_LANE)
        self.laneType = dictionary.get("laneType", "")

        # str # The level up type of the event. Only present if relevant. (Legal values: EVOLVE, NORMAL)
        self.levelUpType = dictionary.get("levelUpType", "")

        # str # The monster type of the event. Only present if relevant. (Legal values: BARON_NASHOR, BLUE_GOLEM, DRAGON, RED_LIZARD, VILEMAW)
        self.monsterType = dictionary.get("monsterType", "")

        # int # The participant ID of the event. Only present if relevant.
        self.participantId = dictionary.get("participantId", 0)

        # str # The point captured in the event. Only present if relevant. (Legal values: POINT_A, POINT_B, POINT_C, POINT_D, POINT_E)
        self.pointCaptured = dictionary.get("pointCaptured", "")

        # Position # The position of the event. Only present if relevant.
        val = dictionary.get("position", None)
        self.position = Position(val) if val and not isinstance(val, Position) else val

        # int # The skill slot of the event. Only present if relevant.
        self.skillSlot = dictionary.get("skillSlot", 0)

        # int # The team ID of the event. Only present if relevant.
        self.teamId = dictionary.get("teamId", 0)

        # int # Represents how many milliseconds into the game the event occurred.
        self.timestamp = dictionary.get("timestamp", 0)

        # str # The tower type of the event. Only present if relevant. (Legal values: BASE_TURRET, FOUNTAIN_TURRET, INNER_TURRET, NEXUS_TURRET, OUTER_TURRET, UNDEFINED_TURRET)
        self.towerType = dictionary.get("towerType", "")

        # int # The victim ID of the event. Only present if relevant.
        self.victimId = dictionary.get("victimId", 0)

        # str # The ward type of the event. Only present if relevant. (Legal values: SIGHT_WARD, TEEMO_MUSHROOM, UNDEFINED, VISION_WARD, YELLOW_TRINKET, YELLOW_TRINKET_UPGRADE)
        self.wardType = dictionary.get("wardType", "")


class ParticipantFrame(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchFrame._id"))

    def __init__(self, dictionary):
        # int # Participant's current gold
        self.currentGold = dictionary.get("currentGold", 0)

        # int # Dominion score of the participant
        self.dominionScore = dictionary.get("dominionScore", 0)

        # int # Number of jungle minions killed by participant
        self.jungleMinionsKilled = dictionary.get("jungleMinionsKilled", 0)

        # int # Participant's current level
        self.level = dictionary.get("level", 0)

        # int # Number of minions killed by participant
        self.minionsKilled = dictionary.get("minionsKilled", 0)

        # int # Participant ID
        self.participantId = dictionary.get("participantId", 0)

        # Position # Participant's position
        val = dictionary.get("position", None)
        self.position = Position(val) if val and not isinstance(val, Position) else val

        # int # Team score of the participant
        self.teamScore = dictionary.get("teamScore", 0)

        # int # Participant's total gold
        self.totalGold = dictionary.get("totalGold", 0)

        # int # Experience earned by participant
        self.xp = dictionary.get("xp", 0)


class Position(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchPosition"
    x = sqlalchemy.Column(sqlalchemy.Integer)
    y = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchEvent._id"))
    _frame_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MatchParticipantFrame._id"))

    def __init__(self, dictionary):
        # int # x position
        self.x = dictionary.get("x", 0)

        # int # y position
        self.y = dictionary.get("y", 0)