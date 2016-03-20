import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.game

try:
    from future.builtins.misc import super
except ImportError:
    pass


@cassiopeia.type.core.common.inheritdocs
class Stats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.game.RawStats

    def __str__(self):
        return "Stats"

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
    def inhibitor_kills(self):
        """
        Returns:
            int: the total number of inhibitors this participant killed
        """
        return self.data.barracksKilled

    @property
    def kills(self):
        """
        Returns:
            int: the total number of kills this participant had
        """
        return self.data.championsKilled

    @property
    def combat_score(self):
        """
        Returns:
            int: dominion only. the part of the participant's score that came from combat-related activities
        """
        return self.data.combatPlayerScore

    @property
    def consumables_bought(self):
        """
        Returns:
            list<Item>: the consumables that the participant bought (careful, they might have just sold them back or hit undo?)
        """
        return self.data.consumablesPurchased

    @property
    def damage_dealt_player(self):
        """
        Returns:
            int: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.damageDealtPlayer

    @property
    def double_kills(self):
        """
        Returns:
            int: the number of double kills this participant had
        """
        return self.data.doubleKills

    @property
    def first_blood(self):
        """
        Returns:
            bool: whether this participant got first blood
        """
        return self.data.firstBlood

    @property
    def gold(self):
        """
        Returns:
            int: the participant's current gold
        """
        return self.data.gold

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
        """
        Returns:
            Item: the participant's sixth item
        """
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
    def tier_3_items_bought(self):
        """
        Returns:
            int: the number of tier 3 items built
        """
        return self.data.legendaryItemsCreated

    @property
    def level(self):
        """
        Returns:
            int: the participant's champion level
        """
        return self.data.level

    @property
    def magic_damage_dealt(self):
        """
        Returns:
            int: the total magic damage this participant dealt
        """
        return self.data.magicDamageDealtPlayer

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
    def minion_denies(self):
        """
        Returns:
            int: the number of minions this participant denied to the enemy. let us know if you figure out what this actually is
        """
        return self.data.minionsDenied

    @property
    def minion_kills(self):
        """
        Returns:
            int: the number of minions this participant killed
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
            int: the number of neutral enemy minions this participant killed
        """
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def ally_monster_kills(self):
        """
        Returns:
            int: the number of neutral ally minions this participant killed
        """
        return self.data.neutralMinionsKilledYourJungle

    @property
    def nexus_killed(self):
        """
        Returns:
            int: the number of nexuses this participant killed
        """
        return self.data.nexusKilled

    @property
    def node_captured(self):
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
    def deaths(self):
        """
        Returns:
            int: the number of deaths this participant had
        """
        return self.data.numDeaths

    @property
    def items_bought(self):
        """
        Returns:
            int: the number of items this participant bought
        """
        return self.data.numItemsBought

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
        return self.data.physicalDamageDealtPlayer

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
    def lane(self):
        """
        Returns:
            Lane: the lane this participant was in
        """
        return cassiopeia.type.core.common.Lane.for_id(self.data.playerPosition) if self.data.playerPosition else None

    @property
    def role(self):
        """
        Returns:
            Role: the role of this particiant
        """
        return cassiopeia.type.core.common.Role.for_id(self.data.playerRole) if self.data.playerRole else None

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
        return self.data.sightWardsBought

    @property
    def q_casts(self):
        """
        Returns:
            int: the number of times this participant cast his Q
        """
        return self.data.spell1Cast

    @property
    def w_casts(self):
        """
        Returns:
            int: the number of tiems this participant cast his W
        """
        return self.data.spell2Cast

    @property
    def e_casts(self):
        """
        Returns:
            int: the number of times this participant cast his E
        """
        return self.data.spell3Cast

    @property
    def r_casts(self):
        """
        Returns:
            int: the number of times this participant cast his R
        """
        return self.data.spell4Cast

    @property
    def d_casts(self):
        """
        Returns:
            int: the number of times this participant cast his D summoner spell
        """
        return self.data.summonSpell1Cast

    @property
    def f_casts(self):
        """
        Returns:
            int: the number of times this participant cast his F summoner spell
        """
        return self.data.summonSpell2Cast

    @property
    def elite_monsters_kills(self):
        """
        Returns:
            int: the number of elite monsters this participant killed
        """
        return self.data.superMonsterKilled

    @property
    def side(self):
        """
        Returns:
            Side: the side the participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.team) if self.data.team else None

    @property
    def objectives(self):
        """
        Returns:
            int: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.teamObjective

    @property
    def time_played(self):
        """
        Returns:
            int: the amount of time this participant played
        """
        return self.data.timePlayed

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
            int: the score for this participant
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
        return self.data.trueDamageDealtPlayer

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
    def turret_kills(self):
        """
        Returns:
            int: the number of turret kills this participant had
        """
        return self.data.turretsKilled

    @property
    def unreal_kills(self):
        """
        Returns:
            int: the number of unreal kills this participant had
        """
        return self.data.unrealKills

    @property
    def victory_points(self):
        """
        Returns:
            int: the number of victory points this participant gained from winning or losing this game
        """
        return self.data.victoryPointTotal

    @property
    def vision_wards_bought(self):
        """
        Returns:
            int: the number of vision wards sprees this participant bought
        """
        return self.data.visionWardsBought

    @property
    def ward_kills(self):
        """
        Returns:
            int: the number of wards sprees this participant killed
        """
        return self.data.wardKilled

    @property
    def wards_placed(self):
        """
        Returns:
            int: the number of wards this participant placed
        """
        return self.data.wardPlaced

    @property
    def win(self):
        """
        Returns:
            bool: whether the participant won the game or not
        """
        return self.data.win


@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.game.Player

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner, champ=self.champion)

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion for this participant
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def summoner(self):
        """
        Returns:
            Summoner: the summoner for this participant
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.summonerId) if self.data.summonerId else None

    @property
    def side(self):
        """
        Returns:
            Side: the side the participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


@cassiopeia.type.core.common.inheritdocs
class Game(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.game.Game

    def __init__(self, data, summoner_id):
        super().__init__(data)
        self.__summoner_id = summoner_id

    def __str__(self):
        return "Game #{id}".format(id=self.id)

    def __iter__(self):
        return iter(self.participants)

    def __len__(self):
        return len(self.participants)

    def __getitem__(self, index):
        return self.participants[index]

    @property
    def summoner(self):
        """
        Returns:
            Summoner: the summoner for this participant
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.__summoner_id) if self.__summoner_id else None

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion for this participant
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """
        Returns:
            datetime: the time when this game was created
        """
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        """
        Returns:
            list<Participant>: the participants in this game
        """
        parts = [Participant(player) for player in self.data.fellowPlayers]
        parts.append(Participant(cassiopeia.type.dto.game.Player({
            "championId": self.data.championId,
            "summonerId": self.__summoner_id,
            "teamId": self.data.teamId
        })))
        return parts

    @property
    def id(self):
        """
        Returns:
            int: the match ID
        """
        return self.data.gameId

    @property
    def mode(self):
        """
        Returns:
            GameMode: the game mode
        """
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def type(self):
        """
        Returns:
            GameType: the game type
        """
        return cassiopeia.type.core.common.GameType(self.data.gameType) if self.data.gameType else None

    @property
    def invalid(self):
        """
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.invalid

    @property
    def ip(self):
        """
        Returns:
            int: the amount of IP the participant gained for this game (the one that this game was pulled using)
        """
        return self.data.ipEarned

    @property
    def level(self):
        """
        Returns:
            int: the participant's champion level
        """
        return self.data.level

    @property
    def map(self):
        """
        Returns:
            Map: the map this game was played on
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def summoner_spell_d(self):
        """
        Returns:
            SummonerSpell: the particpant's first summoner spell (the one that this game was pulled using)
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1) if self.data.spell1 else None

    @property
    def summoner_spell_f(self):
        """
        Returns:
            SummonerSpell: the participant's second summoner spell (the one that this game was pulled using)
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2) if self.data.spell2 else None

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            Stats: the participant's stats (the one that this game was pulled using)
        """
        return Stats(self.data.stats) if self.data.stats else None

    @property
    def sub_type(self):
        """
        Returns:
            SubType: the game's sub-type
        """
        return cassiopeia.type.core.common.SubType(self.data.subType) if self.data.subType else None

    @property
    def side(self):
        """
        Returns:
            Side: the side the participant was on
        """
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Stats.dto_type = cassiopeia.type.dto.game.RawStats
    Participant.dto_type = cassiopeia.type.dto.game.Player
    Game.dto_type = cassiopeia.type.dto.game.Game
