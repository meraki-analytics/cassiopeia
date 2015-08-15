import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.currentgame

class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.currentgame.CurrentGameParticipant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner_name, champ=self.champion)

    @property
    def bot(self):
        return self.data.bot

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        masteries = []
        ranks = []
        for mastery in self.data.masteries:
            masteries.append(mastery.masteryId)
            ranks.append(mastery.rank)
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def profile_icon_id(self):
        return self.data.profileIconId

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        runes = []
        counts = []
        for rune in self.data.runes:
            runes.append(rune.runeId)
            counts.append(rune.count)
        return dict(zip(cassiopeia.riotapi.get_runes(runes), counts))

    @property
    def summoner_spell_d(self):
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1Id) if self.data.spell1Id else None

    @property
    def summoner_spell_f(self):
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2Id) if self.data.spell2Id else None

    @property
    def summoner(self):
        return cassiopeia.riotapi.get_summoner_by_id(self.data.summonerId) if self.data.summonerId else None

    @property
    def summoner_name(self):
        return self.data.summonerName

    @property
    def side(self):
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


class Ban(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.currentgame.BannedChampion

    def __str__(self):
        return "Ban ({champ})".format(champ=self.champion)

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def pick_turn(self):
        return self.data.pickTurn

    @property
    def side(self):
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


class Game(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.currentgame.CurrentGameInfo

    def __str__(self):
        return "Game #{id}".format(id=self.id)

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

    @cassiopeia.type.core.common.lazyproperty
    def bans(self):
        return [Ban(ban) for ban in self.data.bannedChampions]

    @property
    def id(self):
        return self.data.gameId

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        return datetime.timedelta(seconds=self.data.gameLength)

    @property
    def mode(self):
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def queue(self):
        return cassiopeia.type.core.common.Queue.for_id(self.data.gameQueueConfigId) if self.data.gameQueueConfigId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        return datetime.datetime.utcfromtimestamp(self.data.gameStartTime / 1000) if self.data.gameStartTime else None

    @property
    def type(self):
        return cassiopeia.type.core.common.GameType(self.data.gameType) if self.data.gameType else None

    @property
    def map(self):
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def observer_token(self):
        return self.data.observers.encryptionKey

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        return [Participant(participant) for participant in self.data.participants]

    @property
    def platform(self):
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Participant.dto_type = cassiopeia.type.dto.currentgame.CurrentGameParticipant
    Ban.dto_type = cassiopeia.type.dto.currentgame.BannedChampion
    Game.dto_type = cassiopeia.type.dto.currentgame.CurrentGameInfo