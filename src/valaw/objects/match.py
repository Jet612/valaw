from dataclasses import dataclass


@dataclass
class MatchlistEntryDto:
    matchId: str
    gameStartTimeMillis: int
    queueId: str


@dataclass
class MatchlistDto:
    puuid: str
    history: list[MatchlistEntryDto]


@dataclass
class RecentMatchesDto:
    currentTime: int
    matchIds: list[str]


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
    assistants: list[str] | None
    playerLocations: list[PlayerLocationsDto]
    finishingDamage: FinishingDamageDto


@dataclass
class PlayerRoundStatsDto:
    puuid: str
    kills: list[KillDto]
    damage: list[DamageDto]
    score: int
    economy: EconomyDto
    ability: AbilityDto


@dataclass
class RoundResultDto:
    roundNum: int
    roundResult: str
    roundCeremony: str
    winningTeam: str
    bombPlanter: str | None
    bombDefuser: str | None
    plantRoundTime: int | None
    plantPlayerLocations: list[PlayerLocationsDto] | None
    plantLocation: LocationDto | None
    plantSite: str | None
    defuseRoundTime: int | None
    defusePlayerLocations: list[PlayerLocationsDto] | None
    defuseLocation: LocationDto | None
    playerStats: list[PlayerRoundStatsDto]
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
    abilityCasts: AbilityCastsDto | None


@dataclass
class PlayerDto:
    puuid: str
    gameName: str
    tagLine: str
    teamId: str
    partyId: str
    characterId: str
    stats: PlayerStatsDto | None
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
    players: list[PlayerDto]
    coaches: list[CoachDto]
    teams: list[TeamDto]
    roundResults: list[RoundResultDto]
