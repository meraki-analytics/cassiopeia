import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.game

class Stats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.game.RawStats

    def __str__(self):
        return "Stats"

    @property
    def kda(self):
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        return self.data.assists

    @property
    def inhibitor_kills(self):
        return self.data.barracksKilled

    @property
    def kills(self):
        return self.data.championsKilled

    @property
    def combat_score(self):
        return self.data.combatPlayerScore

    @property
    def consumables_bought(self):
        return self.data.consumablesPurchased

    @property
    def damage_dealt(self):
        return self.data.damageDealtPlayer

    @property
    def double_kills(self):
        return self.data.doubleKills

    @property
    def first_blood(self):
        return self.data.firstBlood

    @property
    def gold(self):
        return self.data.gold

    @property
    def gold_earned(self):
        return self.data.goldEarned

    @property
    def gold_spent(self):
        return self.data.goldSpent

    # Item # First item
    @property
    def item0(self):
        return cassiopeia.riotapi.get_item(self.data.item0) if self.data.item0 else None

    # Item # Second item
    @property
    def item1(self):
        return cassiopeia.riotapi.get_item(self.data.item1) if self.data.item1 else None

    # Item # Third item
    @property
    def item2(self):
        return cassiopeia.riotapi.get_item(self.data.item2) if self.data.item2 else None

    # Item # Fourth item
    @property
    def item3(self):
        return cassiopeia.riotapi.get_item(self.data.item3) if self.data.item3 else None

    # Item # Fifth item
    @property
    def item4(self):
        return cassiopeia.riotapi.get_item(self.data.item4) if self.data.item4 else None

    # Item # Sixth item
    @property
    def item5(self):
        return cassiopeia.riotapi.get_item(self.data.item5) if self.data.item5 else None

    # Item # Seventh item
    @property
    def item6(self):
        return cassiopeia.riotapi.get_item(self.data.item6) if self.data.item6 else None

    # list<Item> # Items
    @property
    def items(self):
        return [self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6]

    @property
    def killing_sprees(self):
        return self.data.killingSprees

    @property
    def largest_critical_strike(self):
        return self.data.largestCriticalStrike

    @property
    def largest_killing_spree(self):
        return self.data.largestKillingSpree

    @property
    def largest_multi_kill(self):
        return self.data.largestMultiKill

    @property
    def tier_3_items_bought(self):
        return self.data.legendaryItemsCreated

    @property
    def level(self):
        return self.data.level

    @property
    def magic_damage_dealt(self):
        return self.data.magicDamageDealtPlayer

    @property
    def magic_damage_dealt_to_champions(self):
        return self.data.magicDamageDealtToChampions

    @property
    def magic_damage_taken(self):
        return self.data.magicDamageTaken

    @property
    def minion_denies(self):
        return self.data.minionsDenied

    @property
    def minion_kills(self):
        return self.data.minionsKilled

    @property
    def neutral_minions_kills(self):
        return self.data.neutralMinionsKilled

    @property
    def neutral_minion_kills_enemy_jungle(self):
        return self.data.neutralMinionsKilledEnemyJungle

    @property
    def neutral_minion_kill_ally_jungle(self):
        return self.data.neutralMinionsKilledYourJungle

    @property
    def nexus_killed(self):
        return self.data.nexusKilled

    @property
    def node_captures(self):
        return self.data.nodeCapture

    @property
    def node_capture_assists(self):
        return self.data.nodeCaptureAssist

    @property
    def node_neutralizations(self):
        return self.data.nodeNeutralize

    @property
    def node_neutralization_assists(self):
        return self.data.nodeNeutralizeAssist

    @property
    def deaths(self):
        return self.data.numDeaths

    @property
    def items_bought(self):
        return self.data.numItemsBought

    @property
    def objective_score(self):
        return self.data.objectivePlayerScore

    @property
    def penta_kills(self):
        return self.data.pentaKills

    @property
    def physical_damage_dealt(self):
        return self.data.physicalDamageDealtPlayer

    @property
    def physical_damage_dealt_to_champions(self):
        return self.data.physicalDamageDealtToChampions

    @property
    def physical_damage_taken(self):
        return self.data.physicalDamageTaken

    @property
    def lane(self):
        return cassiopeia.type.core.common.Lane.for_id(self.data.playerPosition) if self.data.playerPosition else None

    @property
    def role(self):
        return cassiopeia.type.core.common.Role.for_id(self.data.playerRole) if self.data.playerRole else None

    @property
    def quadra_kills(self):
        return self.data.quadraKills

    @property
    def sight_wards_bought(self):
        return self.data.sightWardsBought

    @property
    def q_casts(self):
        return self.data.spell1Cast

    @property
    def w_casts(self):
        return self.data.spell2Cast

    @property
    def e_casts(self):
        return self.data.spell3Cast

    @property
    def r_casts(self):
        return self.data.spell4Cast

    @property
    def d_casts(self):
        return self.data.summonSpell1Cast

    @property
    def f_casts(self):
        return self.data.summonSpell2Cast

    @property
    def elite_monsters_kills(self):
        return self.data.superMonsterKilled

    @property
    def side(self):
        return cassiopeia.type.core.common.Side(self.data.team) if self.data.team else None

    @property
    def objectives(self):
        return self.data.teamObjective

    @property
    def time_played(self):
        return self.data.timePlayed

    @property
    def damage_dealt(self):
        return self.data.totalDamageDealt

    @property
    def damage_dealt_to_champions(self):
        return self.data.totalDamageDealtToChampions

    @property
    def damage_taken(self):
        return self.data.totalDamageTaken

    @property
    def healing_done(self):
        return self.data.totalHeal

    @property
    def score(self):
        return self.data.totalPlayerScore

    @property
    def score_rank(self):
        return self.data.totalScoreRank

    @property
    def crowd_control_dealt(self):
        return self.data.totalTimeCrowdControlDealt

    @property
    def units_healed(self):
        return self.data.totalUnitsHealed

    @property
    def triple_kills(self):
        return self.data.tripleKills

    @property
    def true_damage_dealt(self):
        return self.data.trueDamageDealtPlayer

    @property
    def true_damage_dealt_to_champions(self):
        return self.data.trueDamageDealtToChampions

    @property
    def true_damage_taken(self):
        return self.data.trueDamageTaken

    @property
    def turret_kills(self):
        return self.data.turretsKilled

    @property
    def unreal_kills(self):
        return self.data.unrealKills

    @property
    def victory_points(self):
        return self.data.victoryPointTotal

    @property
    def vision_wards_bought(self):
        return self.data.visionWardsBought

    @property
    def ward_kills(self):
        return self.data.wardKilled

    @property
    def wards_placed(self):
        return self.data.wardPlaced

    @property
    def win(self):
        return self.data.win


class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.game.Player

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner, champ=self.champion)

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def summoner(self):
        return cassiopeia.riotapi.get_summoner_by_id(self.data.summonerId) if self.data.summonerId else None

    @property
    def side(self):
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


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
        return cassiopeia.riotapi.get_summoner_by_id(self.__summoner_id) if self.__summoner_id else None

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        parts = [Participant(player) for player in self.data.fellowPlayers]
        parts.append(Participant(cassiopeia.type.dto.game.Player({
            "championId": self.data.championId,
            "summonerId": self.__summoner_id,
            "teamId": self.data.teamId
        })))
        return parts

    @property
    def id(self):
        return self.data.gameId

    @property
    def mode(self):
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def type(self):
        return cassiopeia.type.core.common.GameType(self.data.gameType) if self.data.gameType else None

    @property
    def invalid(self):
        return self.data.invalid

    @property
    def ip(self):
        return self.data.ipEarned

    @property
    def level(self):
        return self.data.level

    @property
    def map(self):
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def summoner_spell_d(self):
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1) if self.data.spell1 else None

    @property
    def summoner_spell_f(self):
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2) if self.data.spell2 else None

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        return Stats(self.data.stats) if self.data.stats else None

    @property
    def sub_type(self):
        return cassiopeia.type.core.common.SubType(self.data.subType) if self.data.subType else None

    @property
    def side(self):
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Stats.dto_type = cassiopeia.type.dto.game.RawStats
    Participant.dto_type = cassiopeia.type.dto.game.Player
    Game.dto_type = cassiopeia.type.dto.game.Game