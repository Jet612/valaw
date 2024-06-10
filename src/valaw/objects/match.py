from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MatchlistEntryDto:
    matchId: str
    gameStartTimeMillis: int
    queueId: str

@dataclass
class MatchlistDto:
    puuid: str
    history: List[MatchlistEntryDto]

@dataclass
class RecentMatchesDto:
    currentTime: int
    matchIds: List[str]

@dataclass
class AbilityDto:
    grenadeEffects: str
    ability1Effects: str
    ability2Effects: str
    ultimateEffects: str

@dataclass
class EconomyDto:
    loadoutValue: int
    weapon: str
    armor: str
    remaining: int
    spent: int

@dataclass
class DamageDto:
    receiver: str
    damage: int
    legshots: int
    bodyshots: int
    headshots: int

@dataclass
class FinishingDamageDto:
    damageType: str
    damageItem: str
    isSecondaryFireMode: bool

@dataclass
class LocationDto:
    x: int
    y: int

@dataclass
class PlayerLocationsDto:
    puuid: str
    viewRadians: float
    location: LocationDto

@dataclass
class KillDto:
    timeSinceGameStartMillis: int
    timeSinceRoundStartMillis: int
    killer: str
    victim: str
    victimLocation: LocationDto
    assistants: Optional[List[str]]
    playerLocations: List[PlayerLocationsDto]
    finishingDamage: FinishingDamageDto

@dataclass
class PlayerRoundStatsDto:
    puuid: str
    kills: List[KillDto]
    damage: List[DamageDto]
    score: int
    economy: EconomyDto
    ability: Optional[AbilityDto]

@dataclass
class RoundResultDto:
    roundNum: int
    roundResult: str
    roundCeremony: str
    winningTeam: str
    bombPlanter: Optional[str]
    bombDefuser: Optional[str]
    plantRoundTime: Optional[int]
    plantPlayerLocations: Optional[List[PlayerLocationsDto]]
    plantLocation: Optional[LocationDto]
    plantSite: Optional[str]
    defuseRoundTime: Optional[int]
    defusePlayerLocations: Optional[List[PlayerLocationsDto]]
    defuseLocation: Optional[LocationDto]
    playerStats: List[PlayerRoundStatsDto]
    roundResultCode: str

@dataclass
class TeamDto:
    teamId: str
    won: bool
    roundsPlayed: int
    roundsWon: int
    numPoints: int

@dataclass
class CoachDto:
    puuid: str
    teamId: str

@dataclass
class AbilityCastsDto:
    grenadeCasts: int
    ability1Casts: int
    ability2Casts: int
    ultimateCasts: int

@dataclass
class PlayerStatsDto:
    score: int
    roundsPlayed: int
    kills: int
    deaths: int
    assists: int
    playtimeMillis: int
    abilityCasts: AbilityCastsDto

@dataclass
class PlayerDto:
    puuid: str
    gameName: str
    tagLine: str
    teamId: str
    partyId: str
    characterId: str
    stats: PlayerStatsDto
    competitiveTier: int
    isObserver: bool
    playerCard: str
    playerTitle: str
    accountLevel: int

@dataclass
class MatchInfoDto:
    matchId: str
    mapId: str
    gameLengthMillis: int
    gameStartMillis: int
    provisioningFlowId: str
    isCompleted: bool
    customGameName: str
    queueId: str
    gameMode: str
    isRanked: bool
    seasonId: str

@dataclass
class MatchDto:
    matchInfo: MatchInfoDto	
    players: List[PlayerDto]	
    coaches: List[CoachDto]	
    teams: List[TeamDto]	
    roundResults: List[RoundResultDto]