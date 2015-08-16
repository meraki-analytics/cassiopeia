import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.currentgame

@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.currentgame.CurrentGameParticipant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner_name, champ=self.champion)

    @property
    def bot(self):
        """Whether the participant is a bot"""
        return self.data.bot

    @property
    def champion(self):
        """The champion this participant is playing"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @cassiopeia.type.core.common.lazyproperty
    def masteries(self):
        """The participant's masteries"""
        masteries = []
        ranks = []
        for mastery in self.data.masteries:
            masteries.append(mastery.masteryId)
            ranks.append(mastery.rank)
        return dict(zip(cassiopeia.riotapi.get_masteries(masteries), ranks))

    @property
    def profile_icon_id(self):
        """The participant's profile icon's ID"""
        return self.data.profileIconId

    @cassiopeia.type.core.common.lazyproperty
    def runes(self):
        """The participant's rune"""
        runes = []
        counts = []
        for rune in self.data.runes:
            runes.append(rune.runeId)
            counts.append(rune.count)
        return dict(zip(cassiopeia.riotapi.get_runes(runes), counts))

    @property
    def summoner_spell_d(self):
        """The participant's first summoner spell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1Id) if self.data.spell1Id else None

    @property
    def summoner_spell_f(self):
        """The participant's second summoner spell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2Id) if self.data.spell2Id else None

    @property
    def summoner(self):
        """The summoner associated with this participant"""
        return cassiopeia.riotapi.get_summoner_by_id(self.data.summonerId) if self.data.summonerId else None

    @property
    def summoner_name(self):
        """The participant's summoner name"""
        return self.data.summonerName

    @property
    def side(self):
        """Which side of the map the participant is on"""
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


@cassiopeia.type.core.common.inheritdocs
class Ban(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.currentgame.BannedChampion

    def __str__(self):
        return "Ban ({champ})".format(champ=self.champion)

    @property
    def champion(self):
        """The champion that was banned"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def pick_turn(self):
        """Which pick turn this ban was on"""
        return self.data.pickTurn

    @property
    def side(self):
        """Which side banned this champion"""
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None


@cassiopeia.type.core.common.inheritdocs
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
        """The bans for this game"""
        return [Ban(ban) for ban in self.data.bannedChampions]

    @property
    def id(self):
        """The game ID"""
        return self.data.gameId

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        """How current duration of the game"""
        return datetime.timedelta(seconds=self.data.gameLength)

    @property
    def mode(self):
        """What game Mode is being played in this game"""
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def queue(self):
        """The Queue type for this game"""
        return cassiopeia.type.core.common.Queue.for_id(self.data.gameQueueConfigId) if self.data.gameQueueConfigId else None

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """The creation timestamp for this game"""
        return datetime.datetime.utcfromtimestamp(self.data.gameStartTime / 1000) if self.data.gameStartTime else None

    @property
    def type(self):
        """The game type"""
        return cassiopeia.type.core.common.GameType(self.data.gameType) if self.data.gameType else None

    @property
    def map(self):
        """The Map for this game"""
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def observer_token(self):
        """The token associated with the observer for this game"""
        return self.data.observers.encryptionKey

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        """The game's participants"""
        return [Participant(participant) for participant in self.data.participants]

    @property
    def platform(self):
        """Which Platform (ie server) the game is being played on"""
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Participant.dto_type = cassiopeia.type.dto.currentgame.CurrentGameParticipant
    Ban.dto_type = cassiopeia.type.dto.currentgame.BannedChampion
    Game.dto_type = cassiopeia.type.dto.currentgame.CurrentGameInfo
