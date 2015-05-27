from cassiopeia.type.dto.common import CassiopeiaDto

class MatchDetail(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Match map ID
        self.mapId = dictionary.get("mapId",0)

        # long # Match creation time. Designates when the team select lobby is created and/or the match is made through match making, not when the game actually starts.
        self.matchCreation = dictionary.get("matchCreation",0)

        # long # Match duration
        self.matchDuration = dictionary.get("matchDuration",0)

        # long # ID of the match
        self.matchId = dictionary.get("matchId",0)

        # string # Match mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.matchMode = dictionary.get("matchMode",'')

        # string # Match type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.matchType = dictionary.get("matchType",'')

        # string # Match version
        self.matchVersion = dictionary.get("matchVersion",'')

        # list<ParticipantIdentity> # Participant identity information
        self.participantIdentities = [ParticipantIdentity(pi) if not isinstance(pi,ParticipantIdentity) else pi for pi in dictionary.get("participantIdentities",[])]

        # list<Participant> # Participant information
        self.participants = [Participant(p) if not isinstance(p,Participant) else p for p in dictionary.get("participants",[])]

        # string # Platform ID of the match
        self.platformId = dictionary.get("platformId",'')

        # string # Match queue type (Legal values: CUSTOM, NORMAL_5x5_BLIND, RANKED_SOLO_5x5, RANKED_PREMADE_5x5, BOT_5x5, NORMAL_3x3, RANKED_PREMADE_3x3, NORMAL_5x5_DRAFT, ODIN_5x5_BLIND, ODIN_5x5_DRAFT, BOT_ODIN_5x5, BOT_5x5_INTRO, BOT_5x5_BEGINNER, BOT_5x5_INTERMEDIATE, RANKED_TEAM_3x3, RANKED_TEAM_5x5, BOT_TT_3x3, GROUP_FINDER_5x5, ARAM_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF_5x5, ONEFORALL_MIRRORMODE_5x5, BOT_URF_5x5, NIGHTMARE_BOT_5x5_RANK1, NIGHTMARE_BOT_5x5_RANK2, NIGHTMARE_BOT_5x5_RANK5, ASCENSION_5x5, HEXAKILL, KING_PORO_5x5, COUNTER_PICK)
        self.queueType = dictionary.get("queueType",'')

        # string # Region where the match was played
        self.region = dictionary.get("region",'')

        # string # Season match was played (Legal values: PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015)
        self.season = dictionary.get("season",'')

        # list<Team> # Team information
        self.teams = [Team(t) if not isinstance(t,Team) else t for t in dictionary.get("teams",[])]

        # Timeline # Match timeline data (not included by default)
        val = dictionary.get("timeline",None)
        self.timeline = Timeline(val) if val and not isinstance(val, Timeline) else val


class Participant(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion ID
        self.championId = dictionary.get("championId",0)

        # string # Highest ranked tier achieved for the previous season, if any, otherwise null. Used to display border in game loading screen. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, UNRANKED)
        self.highestAchievedSeasonTier = dictionary.get("highestAchievedSeasonTier",'')

        # list<Mastery> # List of mastery information
        self.masteries = [Mastery(m) if not isinstance(m,Mastery) else m for m in dictionary.get("masteries",[])]

        # int # Participant ID
        self.participantId = dictionary.get("participantId",0)

        # list<Rune> # List of rune information
        self.runes = [Rune(r) if not isinstance(r,Rune) else r for r in dictionary.get("runes",[])]

        # int # First summoner spell ID
        self.spell1Id = dictionary.get("spell1Id",0)

        # int # Second summoner spell ID
        self.spell2Id = dictionary.get("spell2Id",0)

        # ParticipantStats # Participant statistics
        val = dictionary.get("stats",None)
        self.stats = ParticipantStats(val) if val and not isinstance(val, ParticipantStats) else val

        # int # Team ID
        self.teamId = dictionary.get("teamId",0)

        # ParticipantTimeline # Timeline data. Delta fields refer to values for the specified period (e.g., the gold per minute over the first 10 minutes of the game versus the second 20 minutes of the game. Diffs fields refer to the deltas versus the calculated lane opponent(s).
        val = dictionary.get("timeline",None)
        self.timeline = ParticipantTimeline(val) if val and not isinstance(val, ParticipantTimeline) else val


class ParticipantIdentity(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Participant ID
        self.participantId = dictionary.get("participantId",0)

        # Player # Player information
        val = dictionary.get("player",None)
        self.player = Player(val) if val and not isinstance(val, Player) else val


class Team(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<BannedChampion> # If game was draft mode, contains banned champion data, otherwise null
        self.bans = [BannedChampion(c) if not isinstance(c,BannedChampion) else c for c in dictionary.get("bans",[])]

        # int # Number of times the team killed baron
        self.baronKills = dictionary.get("baronKills",0)

        # long # If game was a dominion game, specifies the points the team had at game end, otherwise null
        self.dominionVictoryScore = dictionary.get("dominionVictoryScore",0)

        # int # Number of times the team killed dragon
        self.dragonKills = dictionary.get("dragonKills",0)

        # boolean # Flag indicating whether or not the team got the first baron kill
        self.firstBaron = dictionary.get("firstBaron",False)

        # boolean # Flag indicating whether or not the team got first blood
        self.firstBlood = dictionary.get("firstBlood",False)

        # boolean # Flag indicating whether or not the team got the first dragon kill
        self.firstDragon = dictionary.get("firstDragon",False)

        # boolean # Flag indicating whether or not the team destroyed the first inhibitor
        self.firstInhibitor = dictionary.get("firstInhibitor",False)

        # boolean # Flag indicating whether or not the team destroyed the first tower
        self.firstTower = dictionary.get("firstTower",False)

        # int # Number of inhibitors the team destroyed
        self.inhibitorKills = dictionary.get("inhibitorKills",0)

        # int # Team ID
        self.teamId = dictionary.get("teamId",0)

        # int # Number of towers the team destroyed
        self.towerKills = dictionary.get("towerKills",0)

        # int # Number of times the team killed vilemaw
        self.vilemawKills = dictionary.get("vilemawKills",0)

        # boolean # Flag indicating whether or not the team won
        self.winner = dictionary.get("winner",False)


class Timeline(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Time between each returned frame in milliseconds.
        self.frameInterval = dictionary.get("frameInterval",0)

        # list<Frame> # List of timeline frames for the game.
        self.frames = [Frame(f) if not isinstance(f,Frame) else f for f in dictionary.get("frames",[])]


class Mastery(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Mastery ID
        self.masteryId = dictionary.get("masteryId",0)

        # long # Mastery rank
        self.rank = dictionary.get("rank",0)


class ParticipantStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Number of assists
        self.assists = dictionary.get("assists",0)

        # long # Champion level achieved
        self.champLevel = dictionary.get("champLevel",0)

        # long # If game was a dominion game, player's combat score, otherwise 0
        self.combatPlayerScore = dictionary.get("combatPlayerScore",0)

        # long # Number of deaths
        self.deaths = dictionary.get("deaths",0)

        # long # Number of double kills
        self.doubleKills = dictionary.get("doubleKills",0)

        # boolean # Flag indicating if participant got an assist on first blood
        self.firstBloodAssist = dictionary.get("firstBloodAssist",False)

        # boolean # Flag indicating if participant got first blood
        self.firstBloodKill = dictionary.get("firstBloodKill",False)

        # boolean # Flag indicating if participant got an assist on the first inhibitor
        self.firstInhibitorAssist = dictionary.get("firstInhibitorAssist",False)

        # boolean # Flag indicating if participant destroyed the first inhibitor
        self.firstInhibitorKill = dictionary.get("firstInhibitorKill",False)

        # boolean # Flag indicating if participant got an assist on the first tower
        self.firstTowerAssist = dictionary.get("firstTowerAssist",False)

        # boolean # Flag indicating if participant destroyed the first tower
        self.firstTowerKill = dictionary.get("firstTowerKill",False)

        # long # Gold earned
        self.goldEarned = dictionary.get("goldEarned",0)

        # long # Gold spent
        self.goldSpent = dictionary.get("goldSpent",0)

        # long # Number of inhibitor kills
        self.inhibitorKills = dictionary.get("inhibitorKills",0)

        # long # First item ID
        self.item0 = dictionary.get("item0",0)

        # long # Second item ID
        self.item1 = dictionary.get("item1",0)

        # long # Third item ID
        self.item2 = dictionary.get("item2",0)

        # long # Fourth item ID
        self.item3 = dictionary.get("item3",0)

        # long # Fifth item ID
        self.item4 = dictionary.get("item4",0)

        # long # Sixth item ID
        self.item5 = dictionary.get("item5",0)

        # long # Seventh item ID
        self.item6 = dictionary.get("item6",0)

        # long # Number of killing sprees
        self.killingSprees = dictionary.get("killingSprees",0)

        # long # Number of kills
        self.kills = dictionary.get("kills",0)

        # long # Largest critical strike
        self.largestCriticalStrike = dictionary.get("largestCriticalStrike",0)

        # long # Largest killing spree
        self.largestKillingSpree = dictionary.get("largestKillingSpree",0)

        # long # Largest multi kill
        self.largestMultiKill = dictionary.get("largestMultiKill",0)

        # long # Magical damage dealt
        self.magicDamageDealt = dictionary.get("magicDamageDealt",0)

        # long # Magical damage dealt to champions
        self.magicDamageDealtToChampions = dictionary.get("magicDamageDealtToChampions",0)

        # long # Magic damage taken
        self.magicDamageTaken = dictionary.get("magicDamageTaken",0)

        # long # Minions killed
        self.minionsKilled = dictionary.get("minionsKilled",0)

        # long # Neutral minions killed
        self.neutralMinionsKilled = dictionary.get("neutralMinionsKilled",0)

        # long # Neutral jungle minions killed in the enemy team's jungle
        self.neutralMinionsKilledEnemyJungle = dictionary.get("neutralMinionsKilledEnemyJungle",0)

        # long # Neutral jungle minions killed in your team's jungle
        self.neutralMinionsKilledTeamJungle = dictionary.get("neutralMinionsKilledTeamJungle",0)

        # long # If game was a dominion game, number of node captures
        self.nodeCapture = dictionary.get("nodeCapture",0)

        # long # If game was a dominion game, number of node capture assists
        self.nodeCaptureAssist = dictionary.get("nodeCaptureAssist",0)

        # long # If game was a dominion game, number of node neutralizations
        self.nodeNeutralize = dictionary.get("nodeNeutralize",0)

        # long # If game was a dominion game, number of node neutralization assists
        self.nodeNeutralizeAssist = dictionary.get("nodeNeutralizeAssist",0)

        # long # If game was a dominion game, player's objectives score, otherwise 0
        self.objectivePlayerScore = dictionary.get("objectivePlayerScore",0)

        # long # Number of penta kills
        self.pentaKills = dictionary.get("pentaKills",0)

        # long # Physical damage dealt
        self.physicalDamageDealt = dictionary.get("physicalDamageDealt",0)

        # long # Physical damage dealt to champions
        self.physicalDamageDealtToChampions = dictionary.get("physicalDamageDealtToChampions",0)

        # long # Physical damage taken
        self.physicalDamageTaken = dictionary.get("physicalDamageTaken",0)

        # long # Number of quadra kills
        self.quadraKills = dictionary.get("quadraKills",0)

        # long # Sight wards purchased
        self.sightWardsBoughtInGame = dictionary.get("sightWardsBoughtInGame",0)

        # long # If game was a dominion game, number of completed team objectives (i.e., quests)
        self.teamObjective = dictionary.get("teamObjective",0)

        # long # Total damage dealt
        self.totalDamageDealt = dictionary.get("totalDamageDealt",0)

        # long # Total damage dealt to champions
        self.totalDamageDealtToChampions = dictionary.get("totalDamageDealtToChampions",0)

        # long # Total damage taken
        self.totalDamageTaken = dictionary.get("totalDamageTaken",0)

        # long # Total heal amount
        self.totalHeal = dictionary.get("totalHeal",0)

        # long # If game was a dominion game, player's total score, otherwise 0
        self.totalPlayerScore = dictionary.get("totalPlayerScore",0)

        # long # If game was a dominion game, team rank of the player's total score (e.g., 1-5)
        self.totalScoreRank = dictionary.get("totalScoreRank",0)

        # long # Total dealt crowd control time
        self.totalTimeCrowdControlDealt = dictionary.get("totalTimeCrowdControlDealt",0)

        # long # Total units healed
        self.totalUnitsHealed = dictionary.get("totalUnitsHealed",0)

        # long # Number of tower kills
        self.towerKills = dictionary.get("towerKills",0)

        # long # Number of triple kills
        self.tripleKills = dictionary.get("tripleKills",0)

        # long # True damage dealt
        self.trueDamageDealt = dictionary.get("trueDamageDealt",0)

        # long # True damage dealt to champions
        self.trueDamageDealtToChampions = dictionary.get("trueDamageDealtToChampions",0)

        # long # True damage taken
        self.trueDamageTaken = dictionary.get("trueDamageTaken",0)

        # long # Number of unreal kills
        self.unrealKills = dictionary.get("unrealKills",0)

        # long # Vision wards purchased
        self.visionWardsBoughtInGame = dictionary.get("visionWardsBoughtInGame",0)

        # long # Number of wards killed
        self.wardsKilled = dictionary.get("wardsKilled",0)

        # long # Number of wards placed
        self.wardsPlaced = dictionary.get("wardsPlaced",0)

        # boolean # Flag indicating whether or not the participant won
        self.winner = dictionary.get("winner",False)


class ParticipantTimeline(CassiopeiaDto):
    def __init__(self, dictionary):
        # ParticipantTimelineData # Ancient golem assists per minute timeline counts
        val = dictionary.get("ancientGolemAssistsPerMinCounts",None)
        self.ancientGolemAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Ancient golem kills per minute timeline counts
        val = dictionary.get("ancientGolemKillsPerMinCounts",None)
        self.ancientGolemKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Assisted lane deaths per minute timeline data
        val = dictionary.get("assistedLaneDeathsPerMinDeltas",None)
        self.assistedLaneDeathsPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Assisted lane kills per minute timeline data
        val = dictionary.get("assistedLaneKillsPerMinDeltas",None)
        self.assistedLaneKillsPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Baron assists per minute timeline counts
        val = dictionary.get("baronAssistsPerMinCounts",None)
        self.baronAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Baron kills per minute timeline counts
        val = dictionary.get("baronKillsPerMinCounts",None)
        self.baronKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Creeps per minute timeline data
        val = dictionary.get("creepsPerMinDeltas",None)
        self.creepsPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Creep score difference per minute timeline data
        val = dictionary.get("csDiffPerMinDeltas",None)
        self.csDiffPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Damage taken difference per minute timeline data
        val = dictionary.get("damageTakenDiffPerMinDeltas",None)
        self.damageTakenDiffPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Damage taken per minute timeline data
        val = dictionary.get("damageTakenPerMinDeltas",None)
        self.damageTakenPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Dragon assists per minute timeline counts
        val = dictionary.get("dragonAssistsPerMinCounts",None)
        self.dragonAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Dragon kills per minute timeline counts
        val = dictionary.get("dragonKillsPerMinCounts",None)
        self.dragonKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Elder lizard assists per minute timeline counts
        val = dictionary.get("elderLizardAssistsPerMinCounts",None)
        self.elderLizardAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Elder lizard kills per minute timeline counts
        val = dictionary.get("elderLizardKillsPerMinCounts",None)
        self.elderLizardKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Gold per minute timeline data
        val = dictionary.get("goldPerMinDeltas",None)
        self.goldPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Inhibitor assists per minute timeline counts
        val = dictionary.get("inhibitorAssistsPerMinCounts",None)
        self.inhibitorAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Inhibitor kills per minute timeline counts
        val = dictionary.get("inhibitorKillsPerMinCounts",None)
        self.inhibitorKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # string # Participant's lane (Legal values: MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM)
        self.lane = dictionary.get("lane",'')

        # string # Participant's role (Legal values: DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT)
        self.role = dictionary.get("role",'')

        # ParticipantTimelineData # Tower assists per minute timeline counts
        val = dictionary.get("towerAssistsPerMinCounts",None)
        self.towerAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Tower kills per minute timeline counts
        val = dictionary.get("towerKillsPerMinCounts",None)
        self.towerKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Tower kills per minute timeline data
        val = dictionary.get("towerKillsPerMinDeltas",None)
        self.towerKillsPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Vilemaw assists per minute timeline counts
        val = dictionary.get("vilemawAssistsPerMinCounts",None)
        self.vilemawAssistsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Vilemaw kills per minute timeline counts
        val = dictionary.get("vilemawKillsPerMinCounts",None)
        self.vilemawKillsPerMinCounts = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Wards placed per minute timeline data
        val = dictionary.get("wardsPerMinDeltas",None)
        self.wardsPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Experience difference per minute timeline data
        val = dictionary.get("xpDiffPerMinDeltas",None)
        self.xpDiffPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val

        # ParticipantTimelineData # Experience per minute timeline data
        val = dictionary.get("xpPerMinDeltas",None)
        self.xpPerMinDeltas = ParticipantTimelineData(val) if val and not isinstance(val, ParticipantTimelineData) else val


class Rune(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Rune rank
        self.rank = dictionary.get("rank",0)

        # long # Rune ID
        self.runeId = dictionary.get("runeId",0)


class Player(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Match history URI
        self.matchHistoryUri = dictionary.get("matchHistoryUri",'')

        # int # Profile icon ID
        self.profileIcon = dictionary.get("profileIcon",0)

        # long # Summoner ID
        self.summonerId = dictionary.get("summonerId",0)

        # string # Summoner name
        self.summonerName = dictionary.get("summonerName",'')


class BannedChampion(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Banned champion ID
        self.championId = dictionary.get("championId",0)

        # int # Turn during which the champion was banned
        self.pickTurn = dictionary.get("pickTurn",0)


class Frame(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Event> # List of events for this frame.
        self.events = [Event(e) if not isinstance(e,Event) else e for e in dictionary.get("events",[])]

        # dict<string, ParticipantFrame> # Map of each participant ID to the participant's information for the frame.
        self.participantFrames = {i:ParticipantFrame(pf) if not isinstance(pf,ParticipantFrame) else pf for i,pf in dictionary.get("participantFrames",{}).iteritems()}

        # long # Represents how many milliseconds into the game the frame occurred.
        self.timestamp = dictionary.get("timestamp",0)


class ParticipantTimelineData(CassiopeiaDto):
    def __init__(self, dictionary):
        # double # Value per minute from 10 min to 20 min
        self.tenToTwenty = dictionary.get("tenToTwenty",0.)

        # double # Value per minute from 30 min to the end of the game
        self.thirtyToEnd = dictionary.get("thirtyToEnd",0.)

        # double # Value per minute from 20 min to 30 min
        self.twentyToThirty = dictionary.get("twentyToThirty",0.)

        # double # Value per minute from the beginning of the game to 10 min
        self.zeroToTen = dictionary.get("zeroToTen",0.)


class Event(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The ascended type of the event. Only present if relevant. Note that CLEAR_ASCENDED refers to when a participants kills the ascended player. (Legal values: CHAMPION_ASCENDED, CLEAR_ASCENDED, MINION_ASCENDED)
        self.ascendedType = dictionary.get("ascendedType",'')

        # list<int> # The assisting participant IDs of the event. Only present if relevant.
        self.assistingParticipantIds = dictionary.get("assistingParticipantIds",[])

        # string # The building type of the event. Only present if relevant. (Legal values: INHIBITOR_BUILDING, TOWER_BUILDING)
        self.buildingType = dictionary.get("buildingType",'')

        # int # The creator ID of the event. Only present if relevant.
        self.creatorId = dictionary.get("creatorId",0)

        # string # Event type. (Legal values: ASCENDED_EVENT, BUILDING_KILL, CAPTURE_POINT, CHAMPION_KILL, ELITE_MONSTER_KILL, ITEM_DESTROYED, ITEM_PURCHASED, ITEM_SOLD, ITEM_UNDO, PORO_KING_SUMMON, SKILL_LEVEL_UP, WARD_KILL, WARD_PLACED)
        self.eventType = dictionary.get("eventType",'')

        # int # The ending item ID of the event. Only present if relevant.
        self.itemAfter = dictionary.get("itemAfter",0)

        # int # The starting item ID of the event. Only present if relevant.
        self.itemBefore = dictionary.get("itemBefore",0)

        # int # The item ID of the event. Only present if relevant.
        self.itemId = dictionary.get("itemId",0)

        # int # The killer ID of the event. Only present if relevant. Killer ID 0 indicates a minion.
        self.killerId = dictionary.get("killerId",0)

        # string # The lane type of the event. Only present if relevant. (Legal values: BOT_LANE, MID_LANE, TOP_LANE)
        self.laneType = dictionary.get("laneType",'')

        # string # The level up type of the event. Only present if relevant. (Legal values: EVOLVE, NORMAL)
        self.levelUpType = dictionary.get("levelUpType",'')

        # string # The monster type of the event. Only present if relevant. (Legal values: BARON_NASHOR, BLUE_GOLEM, DRAGON, RED_LIZARD, VILEMAW)
        self.monsterType = dictionary.get("monsterType",'')

        # int # The participant ID of the event. Only present if relevant.
        self.participantId = dictionary.get("participantId",0)

        # string # The point captured in the event. Only present if relevant. (Legal values: POINT_A, POINT_B, POINT_C, POINT_D, POINT_E)
        self.pointCaptured = dictionary.get("pointCaptured",'')

        # Position # The position of the event. Only present if relevant.
        val = dictionary.get("position",None)
        self.position = Position(val) if val and not isinstance(val, Position) else val

        # int # The skill slot of the event. Only present if relevant.
        self.skillSlot = dictionary.get("skillSlot",0)

        # int # The team ID of the event. Only present if relevant.
        self.teamId = dictionary.get("teamId",0)

        # long # Represents how many milliseconds into the game the event occurred.
        self.timestamp = dictionary.get("timestamp",0)

        # string # The tower type of the event. Only present if relevant. (Legal values: BASE_TURRET, FOUNTAIN_TURRET, INNER_TURRET, NEXUS_TURRET, OUTER_TURRET, UNDEFINED_TURRET)
        self.towerType = dictionary.get("towerType",'')

        # int # The victim ID of the event. Only present if relevant.
        self.victimId = dictionary.get("victimId",0)

        # string # The ward type of the event. Only present if relevant. (Legal values: SIGHT_WARD, TEEMO_MUSHROOM, UNDEFINED, VISION_WARD, YELLOW_TRINKET, YELLOW_TRINKET_UPGRADE)
        self.wardType = dictionary.get("wardType",'')


class ParticipantFrame(CassiopeiaDto):
    def __init__(self, dictionary):
        print(dictionary)
        # int # Participant's current gold
        self.currentGold = dictionary.get("currentGold",0)

        # int # Dominion score of the participant
        self.dominionScore = dictionary.get("dominionScore",0)

        # int # Number of jungle minions killed by participant
        self.jungleMinionsKilled = dictionary.get("jungleMinionsKilled",0)

        # int # Participant's current level
        self.level = dictionary.get("level",0)

        # int # Number of minions killed by participant
        self.minionsKilled = dictionary.get("minionsKilled",0)

        # int # Participant ID
        self.participantId = dictionary.get("participantId",0)

        # Position # Participant's position
        val = dictionary.get("position",None)
        self.position = Position(val) if val and not isinstance(val, Position) else val

        # int # Team score of the participant
        self.teamScore = dictionary.get("teamScore",0)

        # int # Participant's total gold
        self.totalGold = dictionary.get("totalGold",0)

        # int # Experience earned by participant
        self.xp = dictionary.get("xp",0)


class Position(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # x position
        self.x = dictionary.get("x",0)

        # int # y position
        self.y = dictionary.get("y",0)