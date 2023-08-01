from dataclasses import dataclass
from typing import List, Optional

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
    players: List[PlayerDto]
    totalPlayers: int
    immortalStartingPage: int
    immortalStartingIndex: int
    topTierRRThreshold: int
    tierDetails: dict
    startIndex: int
    shard: str
    query: Optional[str]
