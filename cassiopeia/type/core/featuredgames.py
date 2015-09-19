import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.featuredgames

@cassiopeia.type.core.common.inheritdocs
class Participant(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.featuredgames.Participant

    def __str__(self):
        return "{player} ({champ})".format(player=self.summoner_name, champ=self.champion)

    @property
    def bot(self):
        """bool    whether the participant is a bot"""
        return self.data.bot

    @property
    def champion(self):
        """Champion    the champion this participant is playing"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else none

    @property
    def profile_icon_id(self):
        """int    the participant's profile icon's id"""
        return self.data.profileiconid

    @property
    def summoner_spell_d(self):
        """SummonerSpell    the participant's first summonerspell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell1Id) if self.data.spell1Id else none

    @property
    def summoner_spell_f(self):
        """SummonerSpell    the participant's second summonerspell"""
        return cassiopeia.riotapi.get_summoner_spell(self.data.spell2Id) if self.data.spell2Id else none

    @property
    def summoner_name(self):
        """str    the participant's summoner name"""
        return self.data.summonerName

    @property
    def side(self):
        """Side    which side of the map the participant is on"""
        return cassiopeia.type.core.common.side(self.data.teamId) if self.data.teamId else none


@cassiopeia.type.core.common.inheritdocs
class Ban(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.featuredgames.BannedChampion

    def __str__(self):
        return "Ban ({champ})".format(champ=self.champion)

    @property
    def champion(self):
        """Champion    the champion that was banned"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def pick_turn(self):
        """int    which pick turn this ban was on"""
        return self.data.pickTurn

    @property
    def side(self):
        """Side    which side banned this champion"""
        return cassiopeia.type.core.common.Side(self.data.teamId) if self.data.teamId else None
 

@cassiopeia.type.core.common.inheritdocs
class Game(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.featuredgames.FeaturedGameInfo

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
        """list<Ban>    the bans for this game"""
        return [Ban(ban) for ban in self.data.bannedChampions]

    @property
    def id(self):
        """int    the game id"""
        return self.data.gameId

    @cassiopeia.type.core.common.lazyproperty
    def duration(self):
        """timedelta    current duration of the game"""
        return datetime.timedelta(seconds=self.data.gameLength)

    @property
    def mode(self):
        """GameMode    what game mode is being played in this game"""
        return cassiopeia.type.core.common.gamemode(self.data.gameMode) if self.data.gameMode else none

    @property
    def queue(self):
        """Queue    the queue type for this game"""
        return cassiopeia.type.core.common.queue.for_id(self.data.gameQueueConfigId) if self.data.gameQueueConfigId else none

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """datetime    the creation timestamp for this game"""
        return datetime.datetime.utcfromtimestamp(self.data.gameStartTime / 1000) if self.data.gameStartTime else none

    @property
    def type(self):
        """GameType    the game type"""
        return cassiopeia.type.core.common.gametype(self.data.gameType) if self.data.gameType else none

    @property
    def map(self):
        """Map    the map for this game"""
        return cassiopeia.type.core.common.map(self.data.mapId) if self.data.mapId else none

    @property
    def observer_token(self):
        """str    the token associated with the observer for this game"""
        return self.data.observers.encryptionKey

    @cassiopeia.type.core.common.lazyproperty
    def participants(self):
        """list<Participant>    the game's participants"""
        return [Participant(participant) for participant in self.data.participants]

    @property
    def platform(self):
        """Platform    which platform (ie server) the game is being played on"""
        return cassiopeia.type.core.common.Platform(self.data.platformId) if self.data.platformId else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_rebind_all():
    Participant.dto_type = cassiopeia.type.dto.featuredgames.Participant
    Ban.dto_type = cassiopeia.type.dto.featuredgames.BannedChampion
    Game.dto_type = cassiopeia.type.dto.featuredgames.FeaturedGameInfo
