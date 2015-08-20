import datetime

import cassiopeia.riotapi
import cassiopeia.type.dto.common
import cassiopeia.type.core.common
import cassiopeia.type.dto.matchhistory

@cassiopeia.type.core.common.inheritdocs
class MatchSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.matchhistory.MatchSummary

    def __str__(self):
        return "Match {id} Summary".format(id=self.id)

    def __iter__(self):
        return iter(self.participants)

    def __len__(self):
        return len(self.participants)

    def __getitem__(self, index):
        return self.participants[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @cassiopeia.type.core.common.immutablemethod
    def match(self):
        """Gets the full information for this match

        return    Match    the match
        """
        return cassiopeia.riotapi.get_match(self.id)

    @property
    def map(self):
        """Map    the map the match was played on"""
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """datetime    when the match was created"""
        return datetime.datetime.utcfromtimestamp(self.data.matchCreation / 1000) if self.data.matchCreation else None

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        """datetime    duration of the match"""
        return datetime.timedelta(seconds=self.data.matchDuration)

    @property
    def id(self):
        """int    the match ID"""
        return self.data.matchId

    @property
    def mode(self):
        """GameMode    the game mode of the match"""
        return cassiopeia.type.core.common.GameMode(self.data.matchMode) if self.data.matchMode else None

    @property
    def type(self):
        """GameType    the game type"""
        return cassiopeia.type.core.common.GameType(self.data.matchType) if self.data.matchType else None

    @property
    def version(self):
        """str    the patch this match was played in"""
        return self.data.matchVersion

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        """list<Participant>    the participants in this match"""
        participants = []
        for i in range(len(self.data.participants)):
            p = CombinedParticipant(self.data.participants[i], self.data.participantIdentities[i])
            participants.append(Participant(p))
        return sorted(participants, key=lambda p: p.id)

    @property
    def platform(self):
        """Platform    the platform (ie server) for this match"""
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

    @property
    def queue(self):
        """Queue    the queue type for this match"""
        return cassiopeia.type.core.common.Queue(self.data.queueType) if self.data.queueType else None

    @property
    def region(self):
        """Region    the region the match was played in"""
        return cassiopeia.type.core.common.Region(self.data.region) if self.data.region else None

    @property
    def season(self):
        """Season    the season this match was played in"""
        return cassiopeia.type.core.common.Season(self.data.season) if self.data.season else None


@cassiopeia.type.core.common.inheritdocs
class CombinedParticipant(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, participant, identity):
        self.participant = participant
        self.identity = identity


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = CombinedParticipant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner, champ=self.champion)

    @property
    def champion(self):
        """Champion    the champion this participant played"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.participant.championId) if self.data.participant.championId else None

    @property
    def previous_season_tier(self):
        """Tier    the participant's tier last season"""
        return cassiopeia.type.core.common.Tier(self.data.participant.highestAchievedSeasonTier) if self.data.participant.highestAchievedSeasonTier else None

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        """list<Mastery>    the participant's masteries"""
        masteries = []
        ranks = []
        for mastery in self.data.participant.masteries:
            masteries.append(mastery.masteryId)
            ranks.append(mastery.rank)
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def id(self):
        """int    the participant ID"""
        return self.data.participant.participantId

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        """list<Rune>    the participant's current runes"""
        runes = []
        counts = []
        for rune in self.data.participant.runes:
            runes.append(rune.runeId)
            counts.append(rune.rank)
        return dict(zip(cassiopeia.riotapi.get_runes(runes), counts))

    @property
    def summoner_spell_d(self):
        """SummonerSpell    the participant's first summoner spell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell1Id) if self.data.participant.spell1Id else None

    @property
    def summoner_spell_f(self):
        """SummonerSpell    the participant's second summoner spell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell2Id) if self.data.participant.spell2Id else None

    @property
    def stats(self):
        """ParticipantStats    the participant's stats"""
        return ParticipantStats(self.data.participant.stats) if self.data.participant.stats else None

    @property
    def side(self):
        """Side    the side this participant was on"""
        return cassiopeia.type.core.common.Side(self.data.participant.teamId) if self.data.participant.teamId else None

    @cassiopeia.type.core.common.lazyproperty
    def timeline(self):
        """ParticipantTimeline    the participant's timeline"""
        return ParticipantTimeline(self.data.participant.timeline) if self.data.participant.timeline else None

    @property
    def match_history_uri(self):
        """str    the the URI to access this player's match history online"""
        return self.data.identity.player.matchHistoryUri

    @property
    def summoner(self):
        """Summoner    the summoner associated with this participant"""
        return cassiopeia.riotapi.get_summoner_by_id(self.data.identity.player.summonerId) if self.data.identity.player and self.data.identity.player.summonerId else None


@cassiopeia.type.core.common.inheritdocs
class ParticipantStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.matchhistory.ParticipantStats

    def __str__(self):
        return "Participant Stats"

    @property
    def kda(self):
        """float    the participant's kda"""
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        """int    the total number of assists this participant had"""
        return self.data.assists

    @property
    def champion_level(self):
        """int    the champion level of the participant when the game ended"""
        return self.data.champLevel

    @property
    def combat_score(self):
        """int    dominion only. the part of the participant's score that came from combat-related activities"""
        return self.data.combatPlayerScore

    @property
    def deaths(self):
        """int    the number of deaths this participant had"""
        return self.data.deaths

    @property
    def double_kills(self):
        """int    the total number of double kills this participant has had"""
        return self.data.doubleKills

    @property
    def first_blood_assist(self):
        """bool    flag indicating if participant got an assist on first blood"""
        return self.data.firstBloodAssist

    @property
    def first_blood(self):
        """bool    whether this participant got first blood"""
        return self.data.firstBloodKill

    @property
    def first_inhibitor_assist(self):
        """bool    flag indicating if participant got an assist on the first inhibitor"""
        return self.data.firstInhibitorAssist

    @property
    def first_inhibitor(self):
        """bool    flag indicating if participant destroyed the first inhibitor"""
        return self.data.firstInhibitorKill

    @property
    def first_turret_assist(self):
        """bool    flag indicating if participant got an assist on the first tower"""
        return self.data.firstTowerAssist

    @property
    def first_turret(self):
        """bool    flag indicating if participant destroyed the first tower"""
        return self.data.firstTowerKill

    @property
    def gold_earned(self):
        """int    the participant's total gold"""
        return self.data.goldEarned

    @property
    def gold_spent(self):
        """int    the participant's spent gold"""
        return self.data.goldSpent

    @property
    def inhibitor_kills(self):
        """int    the number of inhibitors this participant killed"""
        return self.data.inhibitorKills

    @property
    def item0(self):
        """Item    the participant's first item"""
        return cassiopeia.riotapi.get_item(self.data.item0) if self.data.item0 else None

    @property
    def item1(self):
        """Item    the participant's second item"""
        return cassiopeia.riotapi.get_item(self.data.item1) if self.data.item1 else None

    @property
    def item2(self):
        """Item    the participant's third item"""
        return cassiopeia.riotapi.get_item(self.data.item2) if self.data.item2 else None

    @property
    def item3(self):
        """Item    the participant's fourth item"""
        return cassiopeia.riotapi.get_item(self.data.item3) if self.data.item3 else None

    @property
    def item4(self):
        """Item    the participant's fifth item"""
        return cassiopeia.riotapi.get_item(self.data.item4) if self.data.item4 else None

    @property
    def item5(self):
        return cassiopeia.riotapi.get_item(self.data.item5) if self.data.item5 else None

    @property
    def item6(self):
        """Item    the participant's seventh item (i.e. their ward)"""
        return cassiopeia.riotapi.get_item(self.data.item6) if self.data.item6 else None

    @property
    def items(self):
        """list<Item>    the participant's items"""
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def killing_sprees(self):
        """int    the number of killing sprees this participant had"""
        return self.data.killingSprees

    @property
    def kills(self):
        """int    the total number of champion kills this participant had"""
        return self.data.kills

    @property
    def largest_critical_strike(self):
        """int    the largest critical strike this participant had"""
        return self.data.largestCriticalStrike

    @property
    def largest_killing_spree(self):
        """int    the larges killing spree this participant had"""
        return self.data.largestKillingSpree

    @property
    def largest_multi_kill(self):
        """int    the largest multikill this participant had"""
        return self.data.largestMultiKill

    @property
    def magic_damage_dealt(self):
        """int    the total magic damage this participant dealt"""
        return self.data.magicDamageDealt

    @property
    def magic_damage_dealt_to_champions(self):
        """int    the total magic damage this participant dealt to champions"""
        return self.data.magicDamageDealtToChampions

    @property
    def magic_damage_taken(self):
        """int    the total magic damage this participant received"""
        return self.data.magicDamageTaken

    @property
    def minion_kills(self):
        """int    the number of minions this participant killed"""
        return self.data.minionsKilled

    @property
    def monster_kills(self):
        """int    neutral minions killed"""
        return self.data.neutralMinionsKilled

    @property
    def enemy_monster_kills(self):
        """int    neutral jungle minions killed in the enemy team's jungle"""
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def ally_monster_kills(self):
        """int    neutral jungle minions killed in your team's jungle"""
        return self.data.neutralMinionsKilledTeamJungle

    @property
    def nodes_captured(self):
        """int    dominion only. the number of nodes this participant captured"""
        return self.data.nodeCapture

    @property
    def node_capture_assists(self):
        """int    dominion only. the number of nodes this participant assisted in capturing"""
        return self.data.nodeCaptureAssist

    @property
    def node_neutralizations(self):
        """int    dominion only. the number of nodes this participant neutralized"""
        return self.data.nodeNeutralize

    @property
    def node_neutralization_assists(self):
        """int    dominion only. the number of nodes this participant assisted in neutralizing"""
        return self.data.nodeNeutralizeAssist

    @property
    def objective_score(self):
        """int    dominion only. the part of the participant's score that came from objective-related activities"""
        return self.data.objectivePlayerScore

    @property
    def penta_kills(self):
        """int    the number of penta kills this participant had"""
        return self.data.pentaKills

    @property
    def physical_damage_dealt(self):
        """int    the total amount of physical damage this participant has dealt"""
        return self.data.physicalDamageDealt

    @property
    def physical_damage_dealt_to_champions(self):
        """int    the total physical damage this participant dealt to champions"""
        return self.data.physicalDamageDealtToChampions

    @property
    def physical_damage_taken(self):
        """int    the total physical damage this participant received"""
        return self.data.physicalDamageTaken

    # int # Number of quadra kills
    @property
    def quadra_kills(self):
        """int    the number of quadra kills this participant had"""
        return self.data.quadraKills

    @property
    def sight_wards_bought(self):
        """int    the number of sight wards this participant bought"""
        return self.data.sightWardsBoughtInGame

    @property
    def team_objectives(self):
        """int    if game was a dominion game, number of completed team objectives (i.e., quests)"""
        return self.data.teamObjective

    @property
    def damage_dealt(self):
        """int    the total damage this participant dealt"""
        return self.data.totalDamageDealt

    @property
    def damage_dealt_to_champions(self):
        """int    the total damage this participant dealt to champions"""
        return self.data.totalDamageDealtToChampions

    @property
    def damage_taken(self):
        """int    the total damage this participant received"""
        return self.data.totalDamageTaken

    @property
    def healing_done(self):
        """int    the amount of healing this participant did"""
        return self.data.totalHeal

    @property
    def score(self):
        """int    dominion only. the score for this participant"""
        return self.data.totalPlayerScore

    @property
    def score_rank(self):
        """int    if game was a dominion game, team rank of the player's total score (e.g., 1-5)"""
        return self.data.totalScoreRank

    @property
    def crowd_control_dealt(self):
        """int    the total amount of crowd control this participant dealt (in seconds)"""
        return self.data.totalTimeCrowdControlDealt

    @property
    def units_healed(self):
        """int    the number of units this participant healed"""
        return self.data.totalUnitsHealed

    @property
    def turret_kills(self):
        """int    the number of turret kills this participant had"""
        return self.data.towerKills

    @property
    def triple_kills(self):
        """int    the number of triple kills this participant had"""
        return self.data.tripleKills

    @property
    def true_damage_dealt(self):
        """int    the total true damage this participant dealth"""
        return self.data.trueDamageDealt

    @property
    def true_damage_dealt_to_champions(self):
        """int    the total damage this participant dealt to champions"""
        return self.data.trueDamageDealtToChampions

    @property
    def true_damage_taken(self):
        """int    the total true damage this participant received"""
        return self.data.trueDamageTaken

    @property
    def unreal_kills(self):
        """int    the number of unreal kills this participant had"""
        return self.data.unrealKills

    @property
    def vision_wards_bought(self):
        """int    the number of vision wards sprees this participant bought"""
        return self.data.visionWardsBoughtInGame

    @property
    def ward_kills(self):
        """int    the number of wards sprees this participant killed"""
        return self.data.wardsKilled

    @property
    def wards_placed(self):
        """int    the number of wards this participant placed"""
        return self.data.wardsPlaced

    @property
    def win(self):
        """bool    whether or not the participant won the game"""
        return self.data.winner


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimeline(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.matchhistory.ParticipantTimeline

    def __str__(self):
        return "Participant Timeline"

    @cassiopeia.type.core.common.lazyproperty
    def ancient_golem_assists_per_min_counts(self):
        """ParticipantTimelineData    ancient golem assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.ancientGolemAssistsPerMinCounts) if self.data.ancientGolemAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def ancient_golem_kills_per_min_counts(self):
        """ParticipantTimelineData    ancient golem kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.ancientGolemKillsPerMinCounts) if self.data.ancientGolemKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def assisted_lane_deaths_per_min_deltas(self):
        """ParticipantTimelineData    assisted lane deaths per minute timeline data"""
        return ParticipantTimelineData(self.data.assistedLaneDeathsPerMinDeltas) if self.data.assistedLaneDeathsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def assisted_lane_kills_per_min_deltas(self):
        """ParticipantTimelineData    assisted lane kills per minute timeline data"""
        return ParticipantTimelineData(self.data.assistedLaneKillsPerMinDeltas) if self.data.assistedLaneKillsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def baron_assists_per_min_counts(self):
        """ParticipantTimelineData    baron assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.baronAssistsPerMinCounts) if self.data.baronAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def baron_kills_per_min_counts(self):
        """ParticipantTimelineData    baron kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.baronKillsPerMinCounts) if self.data.baronKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def creeps_per_min_deltas(self):
        """ParticipantTimelineData    creeps per minute timeline data"""
        return ParticipantTimelineData(self.data.creepsPerMinDeltas) if self.data.creepsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def cs_diff_per_min_deltas(self):
        """ParticipantTimelineData    creep score difference per minute timeline data"""
        return ParticipantTimelineData(self.data.csDiffPerMinDeltas) if self.data.csDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def damage_taken_diff_per_min_deltas(self):
        """ParticipantTimelineData    damage taken difference per minute timeline data"""
        return ParticipantTimelineData(self.data.damageTakenDiffPerMinDeltas) if self.data.damageTakenDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def damage_taken_per_min_deltas(self):
        """ParticipantTimelineData    damage taken per minute timeline data"""
        return ParticipantTimelineData(self.data.damageTakenPerMinDeltas) if self.data.damageTakenPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def dragon_assists_per_min_counts(self):
        """ParticipantTimelineData    dragon assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.dragonAssistsPerMinCounts) if self.data.dragonAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def dragon_kills_per_min_counts(self):
        """ParticipantTimelineData    dragon kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.dragonKillsPerMinCounts) if self.data.dragonKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def elder_lizard_assists_per_min_counts(self):
        """ParticipantTimelineData    elder lizard assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.elderLizardAssistsPerMinCounts) if self.data.elderLizardAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def elder_lizard_kills_per_min_counts(self):
        """ParticipantTimelineData    elder lizard kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.elderLizardKillsPerMinCounts) if self.data.elderLizardKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def gold_per_min_deltas(self):
        """ParticipantTimelineData    gold per minute timeline data"""
        return ParticipantTimelineData(self.data.goldPerMinDeltas) if self.data.goldPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def inhibitor_assists_per_min_counts(self):
        """ParticipantTimelineData    inhibitor assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.inhibitorAssistsPerMinCounts) if self.data.inhibitorAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def inhibitor_kills_per_min_counts(self):
        """ParticipantTimelineData    inhibitor kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.inhibitorKillsPerMinCounts) if self.data.inhibitorKillsPerMinCounts else None

    @property
    def lane(self):
        """Lane    the lane this participant was in"""
        lane = self.data.lane
        lane = "MIDDLE" if lane == "MID" else lane
        lane = "BOTTOM" if lane == "BOT" else lane
        return cassiopeia.type.core.common.Lane(lane) if lane else None

    @property
    def role(self):
        """Role    the role of this particiant"""
        return cassiopeia.type.core.common.Role(self.data.role) if self.data.role else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_assists_per_min_counts(self):
        """ParticipantTimelineData    tower assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.towerAssistsPerMinCounts) if self.data.towerAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_kills_per_min_counts(self):
        """ParticipantTimelineData    tower kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.towerKillsPerMinCounts) if self.data.towerKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_Kills_per_min_deltas(self):
        """ParticipantTimelineData    tower kills per minute timeline data"""
        return ParticipantTimelineData(self.data.towerKillsPerMinDeltas) if self.data.towerKillsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def spider_assists_per_min_counts(self):
        """ParticipantTimelineData    vilemaw assists per minute timeline counts"""
        return ParticipantTimelineData(self.data.vilemawAssistsPerMinCounts) if self.data.vilemawAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def spider_kills_per_min_counts(self):
        """ParticipantTimelineData    vilemaw kills per minute timeline counts"""
        return ParticipantTimelineData(self.data.vilemawKillsPerMinCounts) if self.data.vilemawKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def wards_per_min_deltas(self):
        """ParticipantTimelineData    wards placed per minute timeline data"""
        return ParticipantTimelineData(self.data.wardsPerMinDeltas) if self.data.wardsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def xp_diff_per_min_deltas(self):
        """ParticipantTimelineData    experience difference per minute timeline data"""
        return ParticipantTimelineData(self.data.xpDiffPerMinDeltas) if self.data.xpDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def xp_per_min_deltas(self):
        """ParticipantTimelineData    experience per minute timeline data"""
        return ParticipantTimelineData(self.data.xpPerMinDeltas) if self.data.xpPerMinDeltas else None
        

@cassiopeia.type.core.common.inheritdocs
class ParticipantTimelineData(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.matchhistory.ParticipantTimelineData
    
    def __str__(self):
        return "Participant Timeline Data"

    @property
    def ten_to_twenty(self):
        """float    value per minute from 10 min to 20 min"""
        return self.data.tenToTwenty

    @property
    def thirty_to_end(self):
        """float    value per minute from 30 min to the end of the game"""
        return self.data.thirtyToEnd

    @property
    def twenty_to_thirty(self):
        """float    value per minute from 20 min to 30 min"""
        return self.data.twentyToThirty

    @property
    def zero_to_ten(self):
        """float    value per minute from the beginning of the game to 10 min"""
        return self.data.zeroToTen

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_rebind_all():
    MatchSummary.dto_type = cassiopeia.type.dto.matchhistory.MatchSummary
    ParticipantStats.dto_type = cassiopeia.type.dto.matchhistory.ParticipantStats
    ParticipantTimeline.dto_type = cassiopeia.type.dto.matchhistory.ParticipantTimeline
    ParticipantTimelineData.dto_type = cassiopeia.type.dto.matchhistory.ParticipantTimelineData
