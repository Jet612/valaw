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
    competitiveTier: int

@dataclass
class DetailsDto:
    rankedRatingThreshold: int
    startingPage: int
    startingIndex: int

@dataclass
class TierDto:
    tier_24: DetailsDto
    tier_25: DetailsDto
    tier_26: DetailsDto
    tier_27: DetailsDto

@dataclass
class LeaderboardDto:
    actId: str
    players: List[PlayerDto]
    totalPlayers: int
    immortalStartingPage: int
    immortalStartingIndex: int
    topTierRRThreshold: int
    tierDetails: List[TierDto]
    startIndex: int
    query: Optional[str]
    shard: str
