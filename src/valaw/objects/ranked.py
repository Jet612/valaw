from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PlayerDto:
    puuid: Optional[str]
    gameName: Optional[str]
    tagLine: Optional[str]
    leaderboardRank: int
    rankedRating: int
    numberOfWins: int

@dataclass
class LeaderboardDto:
    shard: str
    actId: str
    totalPlayers: int
    players: List[PlayerDto]