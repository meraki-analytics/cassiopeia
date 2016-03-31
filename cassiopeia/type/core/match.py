import datetime

import cassiopeia.riotapi
import cassiopeia.type.dto.common
import cassiopeia.type.core.common
import cassiopeia.type.dto.match

try:
    from future.builtins.misc import super
except ImportError:
    pass


@cassiopeia.type.core.common.inheritdocs
class Match(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.MatchDetail

    def __str__(self):
        return "Match #{id}".format(id=self.id)

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

    @property
    def map(self):
        """
        Returns:
            Map: the map the match was played on
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """
        Returns:
            datetime: when the match was created
        """
        return datetime.datetime.utcfromtimestamp(self.data.matchCreation / 1000) if self.data.matchCreation else None

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        """
        Returns:
            datetime: duration of the match
        """
        return datetime.timedelta(seconds=self.data.matchDuration)

    @property
    def id(self):
        """
        Returns:
            int: the match ID
        """
        return self.data.matchId

    @property
    def mode(self):
        """
        Returns:
            GameMode: the game mode
        """
        return cassiopeia.type.core.common.GameMode(self.data.matchMode) if self.data.matchMode else None

    @property
    def type(self):
        """
        Returns:
            GameType: the game type
        """
        return cassiopeia.type.core.common.GameType(self.data.matchType) if self.data.matchType else None

    @property
    def version(self):
        """
        Returns:
            str: the patch this match was played in
        """
        return self.data.matchVersion

    @cassiopeia.type.core.common.lazyproperty
    #@cassiopeia.type.core.common.indexable([("summoner_name", str), ("summoner_id", int), ("champion.name", str), ("champion.id", int), ("champion", cassiopeia.type.core.staticdata.Champion), ("summoner", cassiopeia.type.core.summoner.Summoner)])
    def participants(self):
        """
        Returns:
            list<Participant>: the participants in this match
        """
        participants = []
        for i in range(len(self.data.participants)):
            p = CombinedParticipant(self.data.participants[i], self.data.participantIdentities[i])
            participants.append(Participant(p))
        return sorted(participants, key=lambda p: p.id)

    @property
    def platform(self):
        """
        Returns:
            Platform: the platform (ie server) for this match
        """
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

    @property
    def queue(self):
        """
        Returns:
            Queue: the queue type for this match
        """
        return cassiopeia.type.core.common.Queue(self.data.queueType) if self.data.queueType else None

    @property
    def region(self):
        """
        Returns:
            Region: the region the match was played in
        """
        return cassiopeia.type.core.common.Region(self.data.region.lower()) if self.data.region else None

    @property
    def season(self):
        """
        Returns:
            Season: the season this match was played in
        """
        return cassiopeia.type.core.common.Season(self.data.season) if self.data.season else None

    @cassiopeia.type.core.common.lazyproperty
    def blue_team(self):
        """
        Returns:
            Team: the blue team
        """
        for team in self.data.teams:
            if team.teamId == cassiopeia.type.core.common.Side.blue.value:
                return Team(team, [part for part in self.participants if part.side is cassiopeia.type.core.common.Side.blue])
        return None

    @cassiopeia.type.core.common.lazyproperty
    def red_team(self):
        """
        Returns:
            Team: the red team
        """
        for team in self.data.teams:
            if team.teamId == cassiopeia.type.core.common.Side.red.value:
                return Team(team, [part for part in self.participants if part.side is cassiopeia.type.core.common.Side.red])
        return None

    @cassiopeia.type.core.common.lazyproperty
    def timeline(self):
        """
        Returns:
            Timeline: the match timeline
        """
        return Timeline(self.data.timeline, self.participants) if self.data.timeline else None

    @cassiopeia.type.core.common.lazyproperty
    def frames(self):
        """
        Returns:
            list<Frame>: the frames in this match
        """
        return self.timeline.frames


@cassiopeia.type.core.common.inheritdocs
class CombinedParticipant(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, participant, identity):
        self.participant = participant
        self.identity = identity


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = CombinedParticipant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner_name, champ=self.champion)

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion this participant played
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.participant.championId) if self.data.participant.championId else None

    @property
    def previous_season_tier(self):
        """
        Returns:
            Tier: the participant's tier last season
        """
        return cassiopeia.type.core.common.Tier(self.data.participant.highestAchievedSeasonTier) if self.data.participant.highestAchievedSeasonTier else None

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        """
        Returns:
            list<Mastery>: the participant's masteries
        """
        masteries = []
        ranks = []
        for mastery in self.data.participant.masteries:
            masteries.append(mastery.masteryId)
            ranks.append(mastery.rank)
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def id(self):
        """
        Returns:
            int: the participant ID
        """
        return self.data.participant.participantId

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        """
        Returns:
            list<Rune>: the participant's current runes
        """
        runes = []
        counts = []
        for rune in self.data.participant.runes:
            runes.append(rune.runeId)
            counts.append(rune.rank)
        return dict(zip(cassiopeia.riotapi.get_runes(runes), counts))

    @property
    def summoner_spell_d(self):
        """
        Returns:
            SummonerSpell: the participant's first summoner spell
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell1Id) if self.data.participant.spell1Id else None

    @property
    def summoner_spell_f(self):
        """
        Returns:
            SummonerSpell: the participant's second summoner spell
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.participant.spell2Id) if self.data.participant.spell2Id else None

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            ParticipantStats: the participant's stats
        """
        return ParticipantStats(self.data.participant.stats) if self.data.participant.stats else None

    @property
    def side(self):
        """
        Returns:
            Side: the side this participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.participant.teamId) if self.data.participant.teamId else None

    @cassiopeia.type.core.common.lazyproperty
    def timeline(self):
        """
        Returns:
            ParticipantTimeline: the participant's timeline
        """
        return ParticipantTimeline(self.data.participant.timeline) if self.data.participant.timeline else None

    @property
    def match_history_uri(self):
        """
        Returns:
            str: the the URI to access this player's match history online
        """
        return self.data.identity.player.matchHistoryUri if self.data.identity.player else None

    @property
    def summoner(self):
        """
        Returns:
            Summoner: the summoner associated with this participant
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.identity.player.summonerId) if self.data.identity.player and self.data.identity.player.summonerId else None

    @property
    def summoner_id(self):
        """
        Returns:
            str: the participant's summoner id
        """
        return self.data.identity.player.summonerId if self.data.identity.player else None

    @property
    def summoner_name(self):
        """
        Returns:
            str: the participant's summoner name
        """
        return self.data.identity.player.summonerName if self.data.identity.player else None


@cassiopeia.type.core.common.inheritdocs
class Team(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.Team

    def __init__(self, data, participants):
        super().__init__(data)
        self.__participants = participants

    def __str__(self):
        return "{side} team: {players}".format(side=self.side, players=self.__participants)

    def __iter__(self):
        return iter(self.__participants)

    def __len__(self):
        return len(self.__participants)

    def __getitem__(self, index):
        return self.__participants[index]

    @property
    def participants(self):
        """
        Returns:
            list<Participant>: the participants on this team
        """
        return self.__participants

    @cassiopeia.type.core.common.lazyproperty
    def bans(self):
        """
        Returns:
            list<Ban>: the bans for this game
        """
        return [Ban(ban) for ban in self.data.bans]

    @property
    def baron_kills(self):
        """
        Returns:
            int: the number of times the team killed Baron
        """
        return self.data.baronKills

    @property
    def victory_score(self):
        """
        Returns:
            int: dominion only, the points the team had at game end
        """
        return self.data.dominionVictoryScore

    @property
    def dragon_kills(self):
        """
        Returns:
            int: the number of times the team killed Dragon
        """
        return self.data.dragonKills

    @property
    def first_baron(self):
        """
        Returns:
            bool: whether or not the team killed the first baron
        """
        return self.data.firstBaron

    @property
    def first_blood(self):
        """
        Returns:
            bool: whether this team got first blood
        """
        return self.data.firstBlood

    @property
    def first_dragon(self):
        """
        Returns:
            bool: whether or not this team killed the first dragon
        """
        return self.data.firstDragon

    @property
    def first_inhibitor(self):
        """
        Returns:
            bool: flag indicating if this team destroyed the first inhibitor
        """
        return self.data.firstInhibitor

    @property
    def first_rift_herald(self):
        """
        Returns:
            bool: flag indicating if this team killed the first rift herald
        """
        return self.data.firstRiftHerald

    @property
    def first_turret(self):
        """
        Returns:
            bool: flag indicating if this team destroyed the first tower
        """
        return self.data.firstTower

    @property
    def inhibitor_kills(self):
        """
        Returns:
            int: the number of inhibitors this team killed
        """
        return self.data.inhibitorKills

    @property
    def rift_herald_kills(self):
        """
        Returns:
            int: the number of rift heralds this team killed
        """
        return self.data.riftHeraldKills

    @property
    def side(self):
        """
        Returns:
            Side: the side this team was on
        """
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None

    @property
    def turret_kills(self):
        """
        Returns:
            int: the number of turret kills this team had
        """
        return self.data.towerKills

    @property
    def vilemaw_kills(self):
        """
        Returns:
            int: the number of times the team has killed Vilemaw
        """
        return self.data.vilemawKills

    @property
    def win(self):
        """
        Returns:
            bool: whether or not the team won the game
        """
        return self.data.winner


@cassiopeia.type.core.common.inheritdocs
class Timeline(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.Timeline

    def __init__(self, data, participants):
        super().__init__(data)
        self.__participants = participants

    def __str__(self):
        return "Timeline"

    def __iter__(self):
        return iter(self.frames)

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, index):
        return self.frames[index]

    @cassiopeia.type.core.common.lazyproperty
    def frame_interval(self):
        """
        Returns:
            timedelta: the number of milliseconds between frames
        """
        return datetime.timedelta(milliseconds=self.data.frameInterval)

    @cassiopeia.type.core.common.lazyproperty
    def frames(self):
        """
        Returns:
            list<Frame>: the frames in this match
        """
        participants = {participant.id: participant for participant in self.__participants}
        value = [Frame(frame, participants) for frame in self.data.frames]
        del self.__participants
        return value


@cassiopeia.type.core.common.inheritdocs
class ParticipantStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantStats

    def __str__(self):
        return "Participant Stats"

    @property
    def kda(self):
        """
        Returns:
            float: the participant's kda
        """
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        """
        Returns:
            int: the total number of assists this participant had
        """
        return self.data.assists

    @property
    def champion_level(self):
        """
        Returns:
            int: the champion level of the participant when the game ended
        """
        return self.data.champLevel

    @property
    def combat_score(self):
        """
        Returns:
            int: dominion only. the part of the participant's score that came from combat-related activities
        """
        return self.data.combatPlayerScore

    @property
    def cs(self):
        return self.minion_kills + self.monster_kills

    @property
    def deaths(self):
        """
        Returns:
            int: the number of deaths this participant had
        """
        return self.data.deaths

    @property
    def double_kills(self):
        """
        Returns:
            int: the number of double kills this participant had
        """
        return self.data.doubleKills

    @property
    def first_blood_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on first blood
        """
        return self.data.firstBloodAssist

    @property
    def first_blood(self):
        """
        Returns:
            bool: whether participant team got first blood
        """
        return self.data.firstBloodKill

    @property
    def first_inhibitor_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on the first inhibitor
        """
        return self.data.firstInhibitorAssist

    @property
    def first_inhibitor(self):
        """
        Returns:
            bool: flag indicating if this participant destroyed the first inhibitor
        """
        return self.data.firstInhibitorKill

    @property
    def first_turret_assist(self):
        """
        Returns:
            bool: flag indicating if participant got an assist on the first tower
        """
        return self.data.firstTowerAssist

    @property
    def first_turret(self):
        """
        Returns:
            bool: flag indicating if this team destroyed the first tower
        """
        return self.data.firstTowerKill

    @property
    def gold_earned(self):
        """
        Returns:
            int: the participant's total gold
        """
        return self.data.goldEarned

    @property
    def gold_spent(self):
        """
        Returns:
            int: the participant's spent gold
        """
        return self.data.goldSpent

    @property
    def inhibitor_kills(self):
        """
        Returns:
            int: the number of inhibitors this team killed
        """
        return self.data.inhibitorKills

    @property
    def item0(self):
        """
        Returns:
            Item: the participant's first item
        """
        return cassiopeia.riotapi.get_item(self.data.item0) if self.data.item0 else None

    @property
    def item1(self):
        """
        Returns:
            Item: the participant's second item
        """
        return cassiopeia.riotapi.get_item(self.data.item1) if self.data.item1 else None

    @property
    def item2(self):
        """
        Returns:
            Item: the participant's third item
        """
        return cassiopeia.riotapi.get_item(self.data.item2) if self.data.item2 else None

    @property
    def item3(self):
        """
        Returns:
            Item: the participant's fourth item
        """
        return cassiopeia.riotapi.get_item(self.data.item3) if self.data.item3 else None

    @property
    def item4(self):
        """
        Returns:
            Item: the participant's fifth item
        """
        return cassiopeia.riotapi.get_item(self.data.item4) if self.data.item4 else None

    @property
    def item5(self):
        return cassiopeia.riotapi.get_item(self.data.item5) if self.data.item5 else None

    @property
    def item6(self):
        """
        Returns:
            Item: the participant's seventh item (i.e. their ward)
        """
        return cassiopeia.riotapi.get_item(self.data.item6) if self.data.item6 else None

    @property
    def items(self):
        """
        Returns:
            list<Item>: the participant's items
        """
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def killing_sprees(self):
        """
        Returns:
            int: the number of killing sprees this participant had
        """
        return self.data.killingSprees

    @property
    def kills(self):
        """
        Returns:
            int: the total number of kills this participant had
        """
        return self.data.kills

    @property
    def largest_critical_strike(self):
        """
        Returns:
            int: the largest critical strike this participant had
        """
        return self.data.largestCriticalStrike

    @property
    def largest_killing_spree(self):
        """
        Returns:
            int: the larges killing spree this participant had
        """
        return self.data.largestKillingSpree

    @property
    def largest_multi_kill(self):
        """
        Returns:
            int: the largest multikill this participant had
        """
        return self.data.largestMultiKill

    @property
    def magic_damage_dealt(self):
        """
        Returns:
            int: the total magic damage this participant dealt
        """
        return self.data.magicDamageDealt

    @property
    def magic_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total magic damage this participant dealt to champions
        """
        return self.data.magicDamageDealtToChampions

    @property
    def magic_damage_taken(self):
        """
        Returns:
            int: the total magic damage this participant received
        """
        return self.data.magicDamageTaken

    @property
    def minion_kills(self):
        """
        Returns:
            int: the number of minions killed
        """
        return self.data.minionsKilled

    @property
    def monster_kills(self):
        """
        Returns:
            int: the number of neutral minions this participant killed
        """
        return self.data.neutralMinionsKilled

    @property
    def enemy_monster_kills(self):
        """
        Returns:
            int: the number of neutral jungle minions killed in the enemy team's jungle
        """
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def ally_monster_kills(self):
        """
        Returns:
            int: the number of neutral jungle minions killed in your team's jungle
        """
        return self.data.neutralMinionsKilledTeamJungle

    @property
    def nodes_captured(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant captured
        """
        return self.data.nodeCapture

    @property
    def node_capture_assists(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant assisted in capturing
        """
        return self.data.nodeCaptureAssist

    @property
    def node_neutralizations(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant neutralized
        """
        return self.data.nodeNeutralize

    @property
    def node_neutralization_assists(self):
        """
        Returns:
            int: dominion only. the number of nodes this participant assisted in neutralizing
        """
        return self.data.nodeNeutralizeAssist

    @property
    def objective_score(self):
        """
        Returns:
            int: dominion only. the part of the participant's score that came from objective-related activities
        """
        return self.data.objectivePlayerScore

    @property
    def penta_kills(self):
        """
        Returns:
            int: the number of penta kills this participant had
        """
        return self.data.pentaKills

    @property
    def physical_damage_dealt(self):
        """
        Returns:
            int: the total physical damage this participant dealt
        """
        return self.data.physicalDamageDealt

    @property
    def physical_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total physical damage this participant dealt to champions
        """
        return self.data.physicalDamageDealtToChampions

    @property
    def physical_damage_taken(self):
        """
        Returns:
            int: the total physical damage this participant received
        """
        return self.data.physicalDamageTaken

    @property
    def quadra_kills(self):
        """
        Returns:
            int: the number of quadra kills this participant had
        """
        return self.data.quadraKills

    @property
    def sight_wards_bought(self):
        """
        Returns:
            int: the number of sight wards this participant bought
        """
        return self.data.sightWardsBoughtInGame

    @property
    def team_objectives(self):
        """
        Returns:
            int: if game was a dominion game, number of completed team objectives (i.e., quests)
        """
        return self.data.teamObjective

    @property
    def damage_dealt(self):
        """
        Returns:
            int: the total damage this participant dealt
        """
        return self.data.totalDamageDealt

    @property
    def damage_dealt_to_champions(self):
        """
        Returns:
            int: the total damage this participant dealt to champions
        """
        return self.data.totalDamageDealtToChampions

    @property
    def damage_taken(self):
        """
        Returns:
            int: the total damage this participant received
        """
        return self.data.totalDamageTaken

    @property
    def healing_done(self):
        """
        Returns:
            int: the amount of healing this participant did
        """
        return self.data.totalHeal

    @property
    def score(self):
        """
        Returns:
            int: dominion only. the score for this participant
        """
        return self.data.totalPlayerScore

    @property
    def score_rank(self):
        """
        Returns:
            int: if game was a dominion game, team rank of the player's total score (e.g., 1-5)
        """
        return self.data.totalScoreRank

    @property
    def crowd_control_dealt(self):
        """
        Returns:
            int: the total amount of crowd control this participant dealt (in seconds)
        """
        return self.data.totalTimeCrowdControlDealt

    @property
    def units_healed(self):
        """
        Returns:
            int: the number of units this participant healed
        """
        return self.data.totalUnitsHealed

    @property
    def turret_kills(self):
        """
        Returns:
            int: the number of turret kills this participant had
        """
        return self.data.towerKills

    @property
    def triple_kills(self):
        """
        Returns:
            int: the number of triple kills this participant had
        """
        return self.data.tripleKills

    @property
    def true_damage_dealt(self):
        """
        Returns:
            int: the total true damage this participant dealth
        """
        return self.data.trueDamageDealt

    @property
    def true_damage_dealt_to_champions(self):
        """
        Returns:
            int: the total damage this participant dealt to champions
        """
        return self.data.trueDamageDealtToChampions

    @property
    def true_damage_taken(self):
        """
        Returns:
            int: the total true damage this participant received
        """
        return self.data.trueDamageTaken

    @property
    def unreal_kills(self):
        """
        Returns:
            int: the number of unreal kills this participant had
        """
        return self.data.unrealKills

    @property
    def vision_wards_bought(self):
        """
        Returns:
            int: the number of vision wards sprees this participant bought
        """
        return self.data.visionWardsBoughtInGame

    @property
    def ward_kills(self):
        """
        Returns:
            int: the number of wards this participant killed
        """
        return self.data.wardsKilled

    @property
    def wards_placed(self):
        """
        Returns:
            int: the number of wards this participant placed
        """
        return self.data.wardsPlaced

    @property
    def win(self):
        """
        Returns:
            bool: whether or not the participant won the game
        """
        return self.data.winner


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimeline(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantTimeline

    def __str__(self):
        return "Participant Timeline"

    @cassiopeia.type.core.common.lazyproperty
    def ancient_golem_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: ancient golem assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.ancientGolemAssistsPerMinCounts) if self.data.ancientGolemAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def ancient_golem_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: ancient golem kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.ancientGolemKillsPerMinCounts) if self.data.ancientGolemKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def assisted_lane_deaths_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: assisted lane deaths per minute timeline data
        """
        return ParticipantTimelineData(self.data.assistedLaneDeathsPerMinDeltas) if self.data.assistedLaneDeathsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def assisted_lane_kills_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: assisted lane kills per minute timeline data
        """
        return ParticipantTimelineData(self.data.assistedLaneKillsPerMinDeltas) if self.data.assistedLaneKillsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def baron_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: baron assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.baronAssistsPerMinCounts) if self.data.baronAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def baron_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: baron kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.baronKillsPerMinCounts) if self.data.baronKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def creeps_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: creeps per minute timeline data
        """
        return ParticipantTimelineData(self.data.creepsPerMinDeltas) if self.data.creepsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def cs_diff_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: creep score difference per minute timeline data
        """
        return ParticipantTimelineData(self.data.csDiffPerMinDeltas) if self.data.csDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def damage_taken_diff_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: damage taken difference per minute timeline data
        """
        return ParticipantTimelineData(self.data.damageTakenDiffPerMinDeltas) if self.data.damageTakenDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def damage_taken_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: damage taken per minute timeline data
        """
        return ParticipantTimelineData(self.data.damageTakenPerMinDeltas) if self.data.damageTakenPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def dragon_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: dragon assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.dragonAssistsPerMinCounts) if self.data.dragonAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def dragon_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: dragon kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.dragonKillsPerMinCounts) if self.data.dragonKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def elder_lizard_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: elder lizard assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.elderLizardAssistsPerMinCounts) if self.data.elderLizardAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def elder_lizard_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: elder lizard kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.elderLizardKillsPerMinCounts) if self.data.elderLizardKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def gold_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: gold per minute timeline data
        """
        return ParticipantTimelineData(self.data.goldPerMinDeltas) if self.data.goldPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def inhibitor_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: inhibitor assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.inhibitorAssistsPerMinCounts) if self.data.inhibitorAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def inhibitor_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: inhibitor kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.inhibitorKillsPerMinCounts) if self.data.inhibitorKillsPerMinCounts else None

    @property
    def lane(self):
        """
        Returns:
            Lane: the lane this participant was in
        """
        lane = self.data.lane
        lane = "MIDDLE" if lane == "MID" else lane
        lane = "BOTTOM" if lane == "BOT" else lane
        return cassiopeia.type.core.common.Lane(lane) if lane else None

    @property
    def role(self):
        """
        Returns:
            Role: the role of this particiant
        """
        return cassiopeia.type.core.common.Role(self.data.role) if self.data.role else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: tower assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.towerAssistsPerMinCounts) if self.data.towerAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: tower kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.towerKillsPerMinCounts) if self.data.towerKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def turret_Kills_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: tower kills per minute timeline data
        """
        return ParticipantTimelineData(self.data.towerKillsPerMinDeltas) if self.data.towerKillsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def spider_assists_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: vilemaw assists per minute timeline counts
        """
        return ParticipantTimelineData(self.data.vilemawAssistsPerMinCounts) if self.data.vilemawAssistsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def spider_kills_per_min_counts(self):
        """
        Returns:
            ParticipantTimelineData: vilemaw kills per minute timeline counts
        """
        return ParticipantTimelineData(self.data.vilemawKillsPerMinCounts) if self.data.vilemawKillsPerMinCounts else None

    @cassiopeia.type.core.common.lazyproperty
    def wards_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: wards placed per minute timeline data
        """
        return ParticipantTimelineData(self.data.wardsPerMinDeltas) if self.data.wardsPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def xp_diff_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: experience difference per minute timeline data
        """
        return ParticipantTimelineData(self.data.xpDiffPerMinDeltas) if self.data.xpDiffPerMinDeltas else None

    @cassiopeia.type.core.common.lazyproperty
    def xp_per_min_deltas(self):
        """
        Returns:
            ParticipantTimelineData: experience per minute timeline data
        """
        return ParticipantTimelineData(self.data.xpPerMinDeltas) if self.data.xpPerMinDeltas else None


@cassiopeia.type.core.common.inheritdocs
class Ban(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.BannedChampion

    def __str__(self):
        return "Ban({champ})".format(champ=self.champion)

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion that was banned
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def pick_turn(self):
        """
        Returns:
            int: which pick turn this ban was on
        """
        return self.data.pickTurn


@cassiopeia.type.core.common.inheritdocs
class Frame(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.Frame
    __participant_quota = 2

    def __init__(self, data, participants):
        super().__init__(data)
        self.__participants = participants
        self.__counter = 0

    def __str__(self):
        return "Frame ({time})".format(time=self.timestamp)

    def __iter__(self):
        return iter(self.events)

    def __len__(self):
        return len(self.events)

    def __getitem__(self, index):
        return self.events[index]

    def __count_participant(self):
        self.__counter += 1
        if self.__counter >= Frame.__participant_quota:
            del self.__counter
            del self.__participants

    @cassiopeia.type.core.common.lazyproperty
    def events(self):
        """
        Returns:
            list<Event>: the events in this frame
        """
        value = [Event(event, self.__participants) for event in self.data.events]
        self.__count_participant()
        return value

    @cassiopeia.type.core.common.lazyproperty
    def participant_frames(self):
        """
        Returns:
            dict<participantID, ParticipantFrame>: the frames in for each participant
        """
        value = {participant: ParticipantFrame(self.data.participantFrames[str(id_)], self.__participants) for id_, participant in self.__participants.items()}
        self.__count_participant()
        return value

    @cassiopeia.type.core.common.lazyproperty
    def timestamp(self):
        """
        Returns:
            datetime: the timestamp for this frame
        """
        return datetime.timedelta(milliseconds=self.data.timestamp)


@cassiopeia.type.core.common.inheritdocs
class ParticipantTimelineData(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantTimelineData

    def __str__(self):
        return "Participant Timeline Data"

    @property
    def ten_to_twenty(self):
        """
        Returns:
            float: value per minute from 10 min to 20 min
        """
        return self.data.tenToTwenty

    @property
    def thirty_to_end(self):
        """
        Returns:
            float: value per minute from 30 min to the end of the game
        """
        return self.data.thirtyToEnd

    @property
    def twenty_to_thirty(self):
        """
        Returns:
            float: value per minute from 20 min to 30 min
        """
        return self.data.twentyToThirty

    @property
    def zero_to_ten(self):
        """
        Returns:
            float: value per minute from the beginning of the game to 10 min
        """
        return self.data.zeroToTen


@cassiopeia.type.core.common.inheritdocs
class Event(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.Event
    __participant_quota = 5

    def __str__(self):
        return "Event ({type})".format(type=self.type)

    def __init__(self, data, participants):
        super().__init__(data)
        self.__participants = participants
        self.__counter = 0

    def __count_participant(self):
        self.__counter += 1
        if self.__counter >= Event.__participant_quota:
            del self.__counter
            del self.__participants

    @property
    def ascended(self):
        """
        Returns:
            Ascended: what died in the event
        """
        return cassiopeia.type.core.common.Ascended(self.data.ascendedType) if self.data.ascendedType else None

    @cassiopeia.type.core.common.lazyproperty
    def assists(self):
        """
        Returns:
            list<Participant>: the participants who assisted in the event
        """
        value = [self.__participants[i] for i in self.data.assistingParticipantIds]
        self.__count_participant()
        return value

    @property
    def building(self):
        """
        Returns:
            Building: the building type associated with the event, if any
        """
        return cassiopeia.type.core.common.Building(self.data.buildingType) if self.data.buildingType else None

    @cassiopeia.type.core.common.lazyproperty
    def creator(self):
        """
        Returns:
            Participant: the participant who created the event
        """
        value = self.__participants[self.data.creatorId] if self.data.creatorId else None
        self.__count_participant()
        return value

    @property
    def type(self):
        """
        Returns:
            EventType: the event type
        """
        return cassiopeia.type.core.common.EventType(self.data.eventType) if self.data.eventType else None

    @property
    def item_after(self):
        """
        Returns:
            Item: the item involved before the event happened
        """
        return cassiopeia.riotapi.get_item(self.data.itemAfter) if self.data.itemAfter else None

    @property
    def item_before(self):
        """
        Returns:
            Item: the item involved after the event happened
        """
        return cassiopeia.riotapi.get_item(self.data.itemBefore) if self.data.itemBefore else None

    @property
    def item(self):
        """
        Returns:
            Item: the item involved in the event
        """
        return cassiopeia.riotapi.get_item(self.data.itemId) if self.data.itemId else None

    @cassiopeia.type.core.common.lazyproperty
    def killer(self):
        """
        Returns:
            Participant: the participant who did the killing
        """
        value = self.__participants[self.data.killerId] if self.data.killerId else None
        self.__count_participant()
        return value

    @property
    def lane(self):
        """
        Returns:
            Lane: the lane this event happened in
        """
        return cassiopeia.type.core.common.LaneType(self.data.laneType) if self.data.laneType else None

    @property
    def level_up(self):
        """
        Returns:
            LevelUp: the level up type of the event
        """
        return cassiopeia.type.core.common.LevelUp(self.data.levelUpType) if self.data.levelUpType else None

    @property
    def monster(self):
        """
        Returns:
            Monster: the monster that was involved in the event
        """
        return cassiopeia.type.core.common.Monster(self.data.monsterType) if self.data.monsterType else None

    @cassiopeia.type.core.common.lazyproperty
    def participant(self):
        """
        Returns:
            Participant: the primary participant that event happened to or who was involved in the event
        """
        value = self.__participants[self.data.participantId] if self.data.participantId else None
        self.__count_participant()
        return value

    @property
    def point_captured(self):
        """
        Returns:
            Point: dominion only, which point was captured
        """
        return cassiopeia.type.core.common.Point(self.data.pointCaptured) if self.data.pointCaptured else None

    @cassiopeia.type.core.common.lazyproperty
    def position(self):
        """
        Returns:
            Position: the position where the event occurred
        """
        return Position(self.data.position) if self.data.position else None

    @property
    def skill_slot(self):
        """
        Returns:
            int: the skill slot of the event
        """
        return self.data.skillSlot

    @property
    def tower(self):
        """
        Returns:
            Tower: which tower was involved in the event
        """
        return cassiopeia.type.core.common.Turret(self.data.towerType) if self.data.teamId else None

    @cassiopeia.type.core.common.lazyproperty
    def timestamp(self):
        """
        Returns:
            datetime: the timestamp for this event
        """
        return datetime.timedelta(milliseconds=self.data.timestamp)

    @property
    def side(self):
        """
        Returns:
            Side: the side this participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.towerType else None

    @cassiopeia.type.core.common.lazyproperty
    def victim(self):
        """
        Returns:
            Participant: the victim!
        """
        value = self.__participants[self.data.victimId] if self.data.victimId else None
        self.__count_participant()
        return value

    @property
    def ward(self):
        """
        Returns:
            Ward: the ward type associated with this event
        """
        return cassiopeia.type.core.common.Ward(self.data.wardType) if self.data.wardType else None


@cassiopeia.type.core.common.inheritdocs
class ParticipantFrame(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.ParticipantFrame

    def __init__(self, data, participants):
        super().__init__(data)
        self.__participant = participants[self.data.participantId]

    def __str__(self):
        return "Participant Frame ({player})".format(player=self.__participant)

    @property
    def gold(self):
        """
        Returns:
            int: the participant's total gold
        """
        return self.data.totalGold

    @property
    def current_gold(self):
        """
        Returns:
            int: the participant's current gold
        """
        return self.data.currentGold

    @property
    def score(self):
        """
        Returns:
            int: dominion only. the score for this participant
        """
        return self.data.dominionScore

    @property
    def jungle_monsters_killed(self):
        """
        Returns:
            int: the number of neutral jungle monsters killed
        """
        return self.data.jungleMinionsKilled

    @property
    def level(self):
        """
        Returns:
            int: the participant's champion level
        """
        return self.data.level

    @property
    def minion_kills(self):
        """
        Returns:
            int: the number of minions killed
        """
        return self.data.minionsKilled

    @property
    def participant(self):
        """
        Returns:
            Participant: the participant whose frames you are looking at
        """
        return self.__participant

    @cassiopeia.type.core.common.lazyproperty
    def position(self):
        """
        Returns:
            Position: the position of the participant
        """
        return Position(self.data.position) if self.data.position else None

    @property
    def team_score(self):
        """
        Returns:
            int: the team score for the participant
        """
        return self.data.teamScore

    @property
    def xp(self):
        """
        Returns:
            int: the amount of XP the participant has
        """
        return self.data.xp


@cassiopeia.type.core.common.inheritdocs
class Position(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.match.Position

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)

    @property
    def x(self):
        """
        Returns:
            int: the x-position of the pixel
        """
        return self.data.x

    @property
    def y(self):
        """
        Returns:
            int: the y-position of the pixel
        """
        return self.data.y


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Match.dto_type = cassiopeia.type.dto.match.MatchDetail
    Team.dto_type = cassiopeia.type.dto.match.Team
    Timeline.dto_type = cassiopeia.type.dto.match.Timeline
    ParticipantStats.dto_type = cassiopeia.type.dto.match.ParticipantStats
    ParticipantTimeline.dto_type = cassiopeia.type.dto.match.ParticipantTimeline
    Ban.dto_type = cassiopeia.type.dto.match.BannedChampion
    Frame.dto_type = cassiopeia.type.dto.match.Frame
    ParticipantTimelineData.dto_type = cassiopeia.type.dto.match.ParticipantTimelineData
    Event.dto_type = cassiopeia.type.dto.match.Event
    ParticipantFrame.dto_type = cassiopeia.type.dto.match.ParticipantFrame
    Position.dto_type = cassiopeia.type.dto.match.Position
