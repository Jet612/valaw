from dataclasses import dataclass


@dataclass
class PlayerDto:
    leaderboardRank: int
    rankedRating: int
    numberOfWins: int
    competitiveTier: int
    puuid: str = ""
    gameName: str = "Private"
    tagLine: str = ""


@dataclass
class LeaderboardDto:
    actId: str
    players: list[PlayerDto]
    totalPlayers: int
    immortalStartingPage: int
    immortalStartingIndex: int
    topTierRRThreshold: int
    tierDetails: dict
    startIndex: int
    shard: str
    query: str | None
