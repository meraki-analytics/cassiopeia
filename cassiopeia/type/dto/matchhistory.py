import cassiopeia.type.dto.common
import cassiopeia.type.core.common

if(cassiopeia.type.dto.common.sqlalchemy_imported):
    import sqlalchemy
    import sqlalchemy.orm

@cassiopeia.type.core.common.inheritdocs
class PlayerHistory(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    matches    list<MatchSummary>    list of matches for the player
    """
    def __init__(self, dictionary):
        self.matches = [(MatchSummary(match) if not isinstance(match, MatchSummary) else match) for match in dictionary.get("matches", []) if match]

    @property
    def champion_ids(self):
        """Gets all champiopn IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.champion_ids
        return ids

    @property
    def item_ids(self):
        """Gets all item IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.item_ids
        return ids

    @property
    def mastery_ids(self):
        """Gets all mastery IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.mastery_ids
        return ids

    @property
    def rune_ids(self):
        """Gets all rune IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.rune_ids
        return ids

    @property
    def summoner_ids(self):
        """Gets all summoner IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.summoner_ids
        return ids

    @property
    def summoner_spell_ids(self):
        """Gets all summoner spell IDs contained in this object"""
        ids = set()
        for m in self.matches:
            ids = ids | m.summoner_spell_ids
        return ids


@cassiopeia.type.core.common.inheritdocs
class MatchSummary(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    mapId                    int                          match map ID
    matchCreation            int                          match creation time. Designates when the team select lobby is created and/or the match is made through match making, not when the game actually starts.
    matchDuration            int                          match duration
    matchId                  int                          ID of the match
    matchMode                str                          match mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
    matchType                str                          match type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
    matchVersion             str                          match version
    participantIdentities    list<ParticipantIdentity>    participant identity information
    participants             list<Participant>            participant information
    platformId               str                          platform ID of the match
    queueType                str                          match queue type (Legal values: CUSTOM, NORMAL_5x5_BLIND, RANKED_SOLO_5x5, RANKED_PREMADE_5x5, BOT_5x5, NORMAL_3x3, RANKED_PREMADE_3x3, NORMAL_5x5_DRAFT, ODIN_5x5_BLIND, ODIN_5x5_DRAFT, BOT_ODIN_5x5, BOT_5x5_INTRO, BOT_5x5_BEGINNER, BOT_5x5_INTERMEDIATE, RANKED_TEAM_3x3, RANKED_TEAM_5x5, BOT_TT_3x3, GROUP_FINDER_5x5, ARAM_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF_5x5, ONEFORALL_MIRRORMODE_5x5, BOT_URF_5x5, NIGHTMARE_BOT_5x5_RANK1, NIGHTMARE_BOT_5x5_RANK2, NIGHTMARE_BOT_5x5_RANK5, ASCENSION_5x5, HEXAKILL, KING_PORO_5x5, COUNTER_PICK)
    region                   str                          region where the match was played
    season                   str                          season match was played (Legal values: PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015)
    """
    def __init__(self, dictionary):
        self.mapId = dictionary.get("mapId", 0)
        self.matchCreation = dictionary.get("matchCreation", 0)
        self.matchDuration = dictionary.get("matchDuration", 0)
        self.matchId = dictionary.get("matchId", 0)
        self.matchMode = dictionary.get("matchMode", "")
        self.matchType = dictionary.get("matchType", "")
        self.matchVersion = dictionary.get("matchVersion", "")
        self.participantIdentities = [(ParticipantIdentity(pi) if not isinstance(pi, ParticipantIdentity) else pi) for pi in dictionary.get("participantIdentities", []) if pi]
        self.participants = [(Participant(p) if not isinstance(p, Participant) else p) for p in dictionary.get("participants", []) if p]
        self.platformId = dictionary.get("platformId", "")
        self.queueType = dictionary.get("queueType", "")
        self.region = dictionary.get("region", "")
        self.season = dictionary.get("season", "")

    @property
    def item_ids(self):
        """Gets all item IDs contained in this object"""
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
        """Gets all champion IDs contained in this object"""
        ids = set()
        for p in self.participants:
            if(p.championId):
                ids.add(p.championId)
        return ids

    @property
    def mastery_ids(self):
        """Gets all mastery IDs contained in this object"""
        ids = set()
        for p in self.participants:
            for m in p.masteries:
                if(m.masteryId):
                    ids.add(m.masteryId)
        return ids

    @property
    def rune_ids(self):
        """Gets all rune IDs contained in this object"""
        ids = set()
        for p in self.participants:
            for r in p.runes:
                if(r.runeId):
                    ids.add(r.runeId)
        return ids

    @property
    def summoner_ids(self):
        """Gets all summoner IDs contained in this object"""
        ids = set()
        for p in self.participantIdentities:
            if(p.player and p.player.summonerId):
                ids.add(p.player.summonerId)
        return ids

    @property
    def summoner_spell_ids(self):
        """Gets all summoner spell IDs contained in this object"""
        ids = set()
        for p in self.participants:
            if(p.spell1Id):
                ids.add(p.spell1Id)
            if(p.spell2Id):
                ids.add(p.spell2Id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    championId                   int                    champion ID
    highestAchievedSeasonTier    str                    highest ranked tier achieved for the previous season, if any, otherwise null. Used to display border in game loading screen. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, UNRANKED)
    masteries                    list<Mastery>          list of mastery information
    participantId                int                    participant ID
    runes                        list<Rune>             list of rune information
    spell1Id                     int                    first summoner spell ID
    spell2Id                     int                    second summoner spell ID
    stats                        ParticipantStats       participant statistics
    teamId                       int                    team ID
    timeline                     ParticipantTimeline    timeline data. Delta fields refer to values for the specified period (e.g., the gold per minute over the first 10 minutes of the game versus the second 20 minutes of the game. Diffs fields refer to the deltas versus the calculated lane opponent(s).
    """
    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.highestAchievedSeasonTier = dictionary.get("highestAchievedSeasonTier", "")
        self.masteries = [(Mastery(m) if not isinstance(m, Mastery) else m) for m in dictionary.get("masteries", []) if m]
        self.participantId = dictionary.get("participantId", 0)
        self.runes = [(Rune(r) if not isinstance(r, Rune) else r) for r in dictionary.get("runes", []) if r]
        self.spell1Id = dictionary.get("spell1Id", 0)
        self.spell2Id = dictionary.get("spell2Id", 0)
        val = dictionary.get("stats", None)
        self.stats = ParticipantStats(val) if val and not isinstance(val, ParticipantStats) else val
        self.teamId = dictionary.get("teamId", 0)
        val = dictionary.get("timeline", None)
        self.timeline = ParticipantTimeline(val) if val and not isinstance(val, ParticipantTimeline) else val


@cassiopeia.type.core.common.inheritdocs
class ParticipantIdentity(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    participantId    int       participant ID
    player           Player    player information
    """
    def __init__(self, dictionary):
        self.participantId = dictionary.get("participantId", 0)
        val = dictionary.get("player", None)
        self.player = Player(val) if val and not isinstance(val, Player) else val


@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    masteryId    int    mastery ID
    rank         int    mastery rank
    """
    def __init__(self, dictionary):
        self.masteryId = dictionary.get("masteryId", 0)
        self.rank = dictionary.get("rank", 0)


@cassiopeia.type.core.common.inheritdocs
class ParticipantStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    assists                            int     number of assists
    champLevel                         int     champion level achieved
    combatPlayerScore                  int     if game was a dominion game, player's combat score, otherwise 0
    deaths                             int     number of deaths
    doubleKills                        int     number of double kills
    firstBloodAssist                   bool    flag indicating if participant got an assist on first blood
    firstBloodKill                     bool    flag indicating if participant got first blood
    firstInhibitorAssist               bool    flag indicating if participant got an assist on the first inhibitor
    firstInhibitorKill                 bool    flag indicating if participant destroyed the first inhibitor
    firstTowerAssist                   bool    flag indicating if participant got an assist on the first tower
    firstTowerKill                     bool    flag indicating if participant destroyed the first tower
    goldEarned                         int     gold earned
    goldSpent                          int     gold spent
    inhibitorKills                     int     number of inhibitor kills
    item0                              int     first item ID
    item1                              int     second item ID
    item2                              int     third item ID
    item3                              int     fourth item ID
    item4                              int     fifth item ID
    item5                              int     sixth item ID
    item6                              int     seventh item ID
    killingSprees                      int     number of killing sprees
    kills                              int     number of kills
    largestCriticalStrike              int     largest critical strike
    largestKillingSpree                int     largest killing spree
    largestMultiKill                   int     largest multi kill
    magicDamageDealt                   int     magical damage dealt
    magicDamageDealtToChampions        int     magical damage dealt to champions
    magicDamageTaken                   int     magic damage taken
    minionsKilled                      int     minions killed
    neutralMinionsKilled               int     neutral minions killed
    neutralMinionsKilledEnemyJungle    int     neutral jungle minions killed in the enemy team's jungle
    neutralMinionsKilledTeamJungle     int     neutral jungle minions killed in your team's jungle
    nodeCapture                        int     if game was a dominion game, number of node captures
    nodeCaptureAssist                  int     if game was a dominion game, number of node capture assists
    nodeNeutralize                     int     if game was a dominion game, number of node neutralizations
    nodeNeutralizeAssist               int     if game was a dominion game, number of node neutralization assists
    objectivePlayerScore               int     if game was a dominion game, player's objectives score, otherwise 0
    pentaKills                         int     number of penta kills
    physicalDamageDealt                int     physical damage dealt
    physicalDamageDealtToChampions     int     physical damage dealt to champions
    physicalDamageTaken                int     physical damage taken
    quadraKills                        int     number of quadra kills
    sightWardsBoughtInGame             int     sight wards purchased
    teamObjective                      int     if game was a dominion game, number of completed team objectives (i.e., quests)
    totalDamageDealt                   int     total damage dealt
    totalDamageDealtToChampions        int     total damage dealt to champions
    totalDamageTaken                   int     total damage taken
    totalHeal                          int     total heal amount
    totalPlayerScore                   int     if game was a dominion game, player's total score, otherwise 0
    totalScoreRank                     int     if game was a dominion game, team rank of the player's total score (e.g., 1-5)
    totalTimeCrowdControlDealt         int     total dealt crowd control time
    totalUnitsHealed                   int     total units healed
    towerKills                         int     number of tower kills
    tripleKills                        int     number of triple kills
    trueDamageDealt                    int     true damage dealt
    trueDamageDealtToChampions         int     true damage dealt to champions
    trueDamageTaken                    int     true damage taken
    unrealKills                        int     number of unreal kills
    visionWardsBoughtInGame            int     vision wards purchased
    wardsKilled                        int     number of wards killed
    wardsPlaced                        int     number of wards placed
    winner                             bool    flag indicating whether or not the participant won
    """
    def __init__(self, dictionary):
        self.assists = dictionary.get("assists", 0)
        self.champLevel = dictionary.get("champLevel", 0)
        self.combatPlayerScore = dictionary.get("combatPlayerScore", 0)
        self.deaths = dictionary.get("deaths", 0)
        self.doubleKills = dictionary.get("doubleKills", 0)
        self.firstBloodAssist = dictionary.get("firstBloodAssist", False)
        self.firstBloodKill = dictionary.get("firstBloodKill", False)
        self.firstInhibitorAssist = dictionary.get("firstInhibitorAssist", False)
        self.firstInhibitorKill = dictionary.get("firstInhibitorKill", False)
        self.firstTowerAssist = dictionary.get("firstTowerAssist", False)
        self.firstTowerKill = dictionary.get("firstTowerKill", False)
        self.goldEarned = dictionary.get("goldEarned", 0)
        self.goldSpent = dictionary.get("goldSpent", 0)
        self.inhibitorKills = dictionary.get("inhibitorKills", 0)
        self.item0 = dictionary.get("item0", 0)
        self.item1 = dictionary.get("item1", 0)
        self.item2 = dictionary.get("item2", 0)
        self.item3 = dictionary.get("item3", 0)
        self.item4 = dictionary.get("item4", 0)
        self.item5 = dictionary.get("item5", 0)
        self.item6 = dictionary.get("item6", 0)
        self.killingSprees = dictionary.get("killingSprees", 0)
        self.kills = dictionary.get("kills", 0)
        self.largestCriticalStrike = dictionary.get("largestCriticalStrike", 0)
        self.largestKillingSpree = dictionary.get("largestKillingSpree", 0)
        self.largestMultiKill = dictionary.get("largestMultiKill", 0)
        self.magicDamageDealt = dictionary.get("magicDamageDealt", 0)
        self.magicDamageDealtToChampions = dictionary.get("magicDamageDealtToChampions", 0)
        self.magicDamageTaken = dictionary.get("magicDamageTaken", 0)
        self.minionsKilled = dictionary.get("minionsKilled", 0)
        self.neutralMinionsKilled = dictionary.get("neutralMinionsKilled", 0)
        self.neutralMinionsKilledEnemyJungle = dictionary.get("neutralMinionsKilledEnemyJungle", 0)
        self.neutralMinionsKilledTeamJungle = dictionary.get("neutralMinionsKilledTeamJungle", 0)
        self.nodeCapture = dictionary.get("nodeCapture", 0)
        self.nodeCaptureAssist = dictionary.get("nodeCaptureAssist", 0)
        self.nodeNeutralize = dictionary.get("nodeNeutralize", 0)
        self.nodeNeutralizeAssist = dictionary.get("nodeNeutralizeAssist", 0)
        self.objectivePlayerScore = dictionary.get("objectivePlayerScore", 0)
        self.pentaKills = dictionary.get("pentaKills", 0)
        self.physicalDamageDealt = dictionary.get("physicalDamageDealt", 0)
        self.physicalDamageDealtToChampions = dictionary.get("physicalDamageDealtToChampions", 0)
        self.physicalDamageTaken = dictionary.get("physicalDamageTaken", 0)
        self.quadraKills = dictionary.get("quadraKills", 0)
        self.sightWardsBoughtInGame = dictionary.get("sightWardsBoughtInGame", 0)
        self.teamObjective = dictionary.get("teamObjective", 0)
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)
        self.totalDamageDealtToChampions = dictionary.get("totalDamageDealtToChampions", 0)
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)
        self.totalHeal = dictionary.get("totalHeal", 0)
        self.totalPlayerScore = dictionary.get("totalPlayerScore", 0)
        self.totalScoreRank = dictionary.get("totalScoreRank", 0)
        self.totalTimeCrowdControlDealt = dictionary.get("totalTimeCrowdControlDealt", 0)
        self.totalUnitsHealed = dictionary.get("totalUnitsHealed", 0)
        self.towerKills = dictionary.get("towerKills", 0)
        self.tripleKills = dictionary.get("tripleKills", 0)
        self.trueDamageDealt = dictionary.get("trueDamageDealt", 0)
        self.trueDamageDealtToChampions = dictionary.get("trueDamageDealtToChampions", 0)
        self.trueDamageTaken = dictionary.get("trueDamageTaken", 0)
        self.unrealKills = dictionary.get("unrealKills", 0)
        self.visionWardsBoughtInGame = dictionary.get("visionWardsBoughtInGame", 0)
        self.wardsKilled = dictionary.get("wardsKilled", 0)
        self.wardsPlaced = dictionary.get("wardsPlaced", 0)
        self.winner = dictionary.get("winner", False)


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimeline(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    ancientGolemAssistsPerMinCounts    ParticipantTimelineData    ancient golem assists per minute timeline counts
    ancientGolemKillsPerMinCounts      ParticipantTimelineData    ancient golem kills per minute timeline counts
    assistedLaneDeathsPerMinDeltas     ParticipantTimelineData    assisted lane deaths per minute timeline data
    assistedLaneKillsPerMinDeltas      ParticipantTimelineData    assisted lane kills per minute timeline data
    baronAssistsPerMinCounts           ParticipantTimelineData    baron assists per minute timeline counts
    baronKillsPerMinCounts             ParticipantTimelineData    baron kills per minute timeline counts
    creepsPerMinDeltas                 ParticipantTimelineData    creeps per minute timeline data
    csDiffPerMinDeltas                 ParticipantTimelineData    creep score difference per minute timeline data
    damageTakenDiffPerMinDeltas        ParticipantTimelineData    damage taken difference per minute timeline data
    damageTakenPerMinDeltas            ParticipantTimelineData    damage taken per minute timeline data
    dragonAssistsPerMinCounts          ParticipantTimelineData    dragon assists per minute timeline counts
    dragonKillsPerMinCounts            ParticipantTimelineData    dragon kills per minute timeline counts
    elderLizardAssistsPerMinCounts     ParticipantTimelineData    elder lizard assists per minute timeline counts
    elderLizardKillsPerMinCounts       ParticipantTimelineData    elder lizard kills per minute timeline counts
    goldPerMinDeltas                   ParticipantTimelineData    gold per minute timeline data
    inhibitorAssistsPerMinCounts       ParticipantTimelineData    inhibitor assists per minute timeline counts
    inhibitorKillsPerMinCounts         ParticipantTimelineData    inhibitor kills per minute timeline counts
    lane                               str                        participant's lane (Legal values: MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM)
    role                               str                        participant's role (Legal values: DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT)
    towerAssistsPerMinCounts           ParticipantTimelineData    tower assists per minute timeline counts
    towerKillsPerMinCounts             ParticipantTimelineData    tower kills per minute timeline counts
    towerKillsPerMinDeltas             ParticipantTimelineData    tower kills per minute timeline data
    vilemawAssistsPerMinCounts         ParticipantTimelineData    vilemaw assists per minute timeline counts
    vilemawKillsPerMinCounts           ParticipantTimelineData    vilemaw kills per minute timeline counts
    wardsPerMinDeltas                  ParticipantTimelineData    wards placed per minute timeline data
    xpDiffPerMinDeltas                 ParticipantTimelineData    experience difference per minute timeline data
    xpPerMinDeltas                     ParticipantTimelineData    experience per minute timeline data
    """
    def __init__(self, dictionary):
        val = dictionary.get("ancientGolemAssistsPerMinCounts", None)
        self.ancientGolemAssistsPerMinCounts = ParticipantTimelineData(val, "ancientGolemAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("ancientGolemKillsPerMinCounts", None)
        self.ancientGolemKillsPerMinCounts = ParticipantTimelineData(val, "ancientGolemKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("assistedLaneDeathsPerMinDeltas", None)
        self.assistedLaneDeathsPerMinDeltas = ParticipantTimelineData(val, "assistedLaneDeathsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("assistedLaneKillsPerMinDeltas", None)
        self.assistedLaneKillsPerMinDeltas = ParticipantTimelineData(val, "assistedLaneKillsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("baronAssistsPerMinCounts", None)
        self.baronAssistsPerMinCounts = ParticipantTimelineData(val, "baronAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("baronKillsPerMinCounts", None)
        self.baronKillsPerMinCounts = ParticipantTimelineData(val, "baronKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("creepsPerMinDeltas", None)
        self.creepsPerMinDeltas = ParticipantTimelineData(val, "creepsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("csDiffPerMinDeltas", None)
        self.csDiffPerMinDeltas = ParticipantTimelineData(val, "csDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("damageTakenDiffPerMinDeltas", None)
        self.damageTakenDiffPerMinDeltas = ParticipantTimelineData(val, "damageTakenDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("damageTakenPerMinDeltas", None)
        self.damageTakenPerMinDeltas = ParticipantTimelineData(val, "damageTakenPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("dragonAssistsPerMinCounts", None)
        self.dragonAssistsPerMinCounts = ParticipantTimelineData(val, "dragonAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("dragonKillsPerMinCounts", None)
        self.dragonKillsPerMinCounts = ParticipantTimelineData(val, "dragonKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("elderLizardAssistsPerMinCounts", None)
        self.elderLizardAssistsPerMinCounts = ParticipantTimelineData(val, "elderLizardAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("elderLizardKillsPerMinCounts", None)
        self.elderLizardKillsPerMinCounts = ParticipantTimelineData(val, "elderLizardKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("goldPerMinDeltas", None)
        self.goldPerMinDeltas = ParticipantTimelineData(val, "goldPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("inhibitorAssistsPerMinCounts", None)
        self.inhibitorAssistsPerMinCounts = ParticipantTimelineData(val, "inhibitorAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("inhibitorKillsPerMinCounts", None)
        self.inhibitorKillsPerMinCounts = ParticipantTimelineData(val, "inhibitorKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        self.lane = dictionary.get("lane", "")
        self.role = dictionary.get("role", "")
        val = dictionary.get("towerAssistsPerMinCounts", None)
        self.towerAssistsPerMinCounts = ParticipantTimelineData(val, "towerAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("towerKillsPerMinCounts", None)
        self.towerKillsPerMinCounts = ParticipantTimelineData(val, "towerKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("towerKillsPerMinDeltas", None)
        self.towerKillsPerMinDeltas = ParticipantTimelineData(val, "towerKillsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("vilemawAssistsPerMinCounts", None)
        self.vilemawAssistsPerMinCounts = ParticipantTimelineData(val, "vilemawAssistsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("vilemawKillsPerMinCounts", None)
        self.vilemawKillsPerMinCounts = ParticipantTimelineData(val, "vilemawKillsPerMinCounts") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("wardsPerMinDeltas", None)
        self.wardsPerMinDeltas = ParticipantTimelineData(val, "wardsPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("xpDiffPerMinDeltas", None)
        self.xpDiffPerMinDeltas = ParticipantTimelineData(val, "xpDiffPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val
        val = dictionary.get("xpPerMinDeltas", None)
        self.xpPerMinDeltas = ParticipantTimelineData(val, "xpPerMinDeltas") if val and not isinstance(val, ParticipantTimelineData) else val


@cassiopeia.type.core.common.inheritdocs
class Rune(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    rank      int    rune rank
    runeId    int    rune ID
    """
    def __init__(self, dictionary):
        self.rank = dictionary.get("rank", 0)
        self.runeId = dictionary.get("runeId", 0)


@cassiopeia.type.core.common.inheritdocs
class Player(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    matchHistoryUri    str    match history URI
    profileIcon        int    profile icon ID
    summonerId         int    summoner ID
    summonerName       str    summoner name
    """
    def __init__(self, dictionary):
        self.matchHistoryUri = dictionary.get("matchHistoryUri", "")
        self.profileIcon = dictionary.get("profileIcon", 0)
        self.summonerId = dictionary.get("summonerId", 0)
        self.summonerName = dictionary.get("summonerName", "")


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimelineData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    tenToTwenty       float    value per minute from 10 min to 20 min
    thirtyToEnd       float    value per minute from 30 min to the end of the game
    twentyToThirty    float    value per minute from 20 min to 30 min
    zeroToTen         float    value per minute from 20 min to 30 min
    """
    def __init__(self, dictionary, type_=None):
        self.tenToTwenty = dictionary.get("tenToTwenty", 0.0)
        self.thirtyToEnd = dictionary.get("thirtyToEnd", 0.0)
        self.twentyToThirty = dictionary.get("twentyToThirty", 0.0)
        self.zeroToTen = dictionary.get("zeroToTen", 0.0)
        self._type = type_

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