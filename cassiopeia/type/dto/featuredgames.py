from cassiopeia.type.dto.common import CassiopeiaDto

class Participant(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Flag indicating whether or not this participant is a bot
        self.bot = dictionary["bot"]

        # long # The ID of the champion played by this participant
        self.championId = dictionary["championId"]

        # long # The ID of the profile icon used by this participant
        self.profileIconId = dictionary["profileIconId"]

        # long # The ID of the first summoner spell used by this participant
        self.spell1Id = dictionary["spell1Id"]

        # long # The ID of the second summoner spell used by this participant
        self.spell2Id = dictionary["spell2Id"]

        # string # The summoner name of this participant
        self.summonerName = dictionary["summonerName"]

        # long # The team ID of this participant, indicating the participant's team
        self.teamId = dictionary["teamId"]


class Observer(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Key used to decrypt the spectator grid game data for playback
        self.encryptionKey = dictionary["encryptionKey"]


class BannedChampion(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # The ID of the banned champion
        self.championId = dictionary["championId"]

        # int # The turn during which the champion was banned
        self.pickTurn = dictionary["pickTurn"]

        # long # The ID of the team that banned the champion
        self.teamId = dictionary["teamId"]


class FeaturedGameInfo(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<BannedChampion> # Banned champion information
        self.bannedChampions = [BannedChampion(ban) if not isinstance(ban, BannedChampion) else ban for ban in dictionary["bannedChampions"]]

        # long # The ID of the game
        self.gameId = dictionary["gameId"]

        # long # The amount of time in seconds that has passed since the game started
        self.gameLength = dictionary["gameLength"]

        # string # The game mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.gameMode = dictionary["gameMode"]

        # long # The queue type (queue types are documented on the Game Constants page)
        self.gameQueueConfigId = dictionary["gameQueueConfigId"]

        # long # The game start time represented in epoch milliseconds
        self.gameStartTime = dictionary["gameStartTime"]

        # string # The game type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.gameType = dictionary["gameType"]

        # long # The ID of the map
        self.mapId = dictionary["mapId"]

        # Observer # The observer information
        self.observers = Observer(dictionary["observers"]) if not isinstance(dictionary["observers"], Observer) else dictionary["observers"]

        # list<Participant> # The participant information
        self.participants = [Participant(participant) if not isinstance(participant, BannedChampion) else participant for participant in dictionary["participants"]]

        # string # The ID of the platform on which the game is being played
        self.platformId = dictionary["platformId"]


class FeaturedGames(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # The suggested interval to wait before requesting FeaturedGames again
        self.clientRefreshInterval = dictionary["clientRefreshInterval"]

        # list<FeaturedGameInfo> # The list of featured games
        self.gameList = [FeaturedGameInfo(game) if not isinstance(game, FeaturedGameInfo) else game for game in dictionary["gameList"]]