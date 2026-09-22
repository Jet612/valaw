from dataclasses import dataclass


@dataclass
class AccountDto:
    puuid: str
    gameName: str | None = None
    tagLine: str | None = None


@dataclass
class ActiveShardDto:
    puuid: str
    game: str
    activeShard: str
