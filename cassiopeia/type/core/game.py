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
            float: the participant's kda
        """
        return self.data.assists

    @property
    def inhibitor_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.barracksKilled

    @property
    def kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.championsKilled

    @property
    def combat_score(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.combatPlayerScore

    @property
    def consumables_bought(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.consumablesPurchased

    @property
    def damage_dealt_player(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.damageDealtPlayer

    @property
    def double_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.doubleKills

    @property
    def first_blood(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.firstBlood

    @property
    def gold(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.gold

    @property
    def gold_earned(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.goldEarned

    @property
    def gold_spent(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.goldSpent

    @property
    def item0(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item0) if self.data.item0 else None

    @property
    def item1(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item1) if self.data.item1 else None

    @property
    def item2(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item2) if self.data.item2 else None

    @property
    def item3(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item3) if self.data.item3 else None

    @property
    def item4(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item4) if self.data.item4 else None

    @property
    def item5(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item5) if self.data.item5 else None

    @property
    def item6(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_item(self.data.item6) if self.data.item6 else None

    @property
    def items(self):
        """
        Returns:
            float: the participant's kda
        """
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def killing_sprees(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.killingSprees

    @property
    def largest_critical_strike(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.largestCriticalStrike

    @property
    def largest_killing_spree(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.largestKillingSpree

    @property
    def largest_multi_kill(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.largestMultiKill

    @property
    def tier_3_items_bought(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.legendaryItemsCreated

    @property
    def level(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.level

    @property
    def magic_damage_dealt(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.magicDamageDealtPlayer

    @property
    def magic_damage_dealt_to_champions(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.magicDamageDealtToChampions

    @property
    def magic_damage_taken(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.magicDamageTaken

    @property
    def minion_denies(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.minionsDenied

    @property
    def minion_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.minionsKilled

    @property
    def monster_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.neutralMinionsKilled

    @property
    def enemy_monster_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def ally_monster_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.neutralMinionsKilledYourJungle

    @property
    def nexus_killed(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.nexusKilled

    @property
    def node_captured(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.nodeCapture

    @property
    def node_capture_assists(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.nodeCaptureAssist

    @property
    def node_neutralizations(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.nodeNeutralize

    @property
    def node_neutralization_assists(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.nodeNeutralizeAssist

    @property
    def deaths(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.numDeaths

    @property
    def items_bought(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.numItemsBought

    @property
    def objective_score(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.objectivePlayerScore

    @property
    def penta_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.pentaKills

    @property
    def physical_damage_dealt(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.physicalDamageDealtPlayer

    @property
    def physical_damage_dealt_to_champions(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.physicalDamageDealtToChampions

    @property
    def physical_damage_taken(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.physicalDamageTaken

    @property
    def lane(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.Lane.for_id(self.data.playerPosition) if self.data.playerPosition else None

    @property
    def role(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.Role.for_id(self.data.playerRole) if self.data.playerRole else None

    @property
    def quadra_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.quadraKills

    @property
    def sight_wards_bought(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.sightWardsBought

    @property
    def q_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.spell1Cast

    @property
    def w_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.spell2Cast

    @property
    def e_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.spell3Cast

    @property
    def r_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.spell4Cast

    @property
    def d_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.summonSpell1Cast

    @property
    def f_casts(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.summonSpell2Cast

    @property
    def elite_monsters_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.superMonsterKilled

    @property
    def side(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.Side(self.data.team) if self.data.team else None

    @property
    def objectives(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.teamObjective

    @property
    def time_played(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.timePlayed

    @property
    def damage_dealt(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalDamageDealt

    @property
    def damage_dealt_to_champions(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalDamageDealtToChampions

    @property
    def damage_taken(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalDamageTaken

    @property
    def healing_done(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalHeal

    @property
    def score(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalPlayerScore

    @property
    def score_rank(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalScoreRank

    @property
    def crowd_control_dealt(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalTimeCrowdControlDealt

    @property
    def units_healed(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.totalUnitsHealed

    @property
    def triple_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.tripleKills

    @property
    def true_damage_dealt(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.trueDamageDealtPlayer

    @property
    def true_damage_dealt_to_champions(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.trueDamageDealtToChampions

    @property
    def true_damage_taken(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.trueDamageTaken

    @property
    def turret_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.turretsKilled

    @property
    def unreal_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.unrealKills

    @property
    def victory_points(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.victoryPointTotal

    @property
    def vision_wards_bought(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.visionWardsBought

    @property
    def ward_kills(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.wardKilled

    @property
    def wards_placed(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.wardPlaced

    @property
    def win(self):
        """
        Returns:
            float: the participant's kda
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
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def summoner(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.summonerId) if self.data.summonerId else None

    @property
    def side(self):
        """
        Returns:
            float: the participant's kda
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
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.__summoner_id) if self.__summoner_id else None

    @property
    def champion(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """
        Returns:
            float: the participant's kda
        """
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        """
        Returns:
            float: the participant's kda
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
            float: the participant's kda
        """
        return self.data.gameId

    @property
    def mode(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def type(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.GameType(self.data.gameType) if self.data.gameType else None

    @property
    def invalid(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.invalid

    @property
    def ip(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.ipEarned

    @property
    def level(self):
        """
        Returns:
            float: the participant's kda
        """
        return self.data.level

    @property
    def map(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def summoner_spell_d(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1) if self.data.spell1 else None

    @property
    def summoner_spell_f(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2) if self.data.spell2 else None

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            float: the participant's kda
        """
        return Stats(self.data.stats) if self.data.stats else None

    @property
    def sub_type(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.SubType(self.data.subType) if self.data.subType else None

    @property
    def side(self):
        """
        Returns:
            float: the participant's kda
        """
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Stats.dto_type = cassiopeia.type.dto.game.RawStats
    Participant.dto_type = cassiopeia.type.dto.game.Player
    Game.dto_type = cassiopeia.type.dto.game.Game
