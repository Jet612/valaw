from dataclasses import dataclass

@dataclass
class AccountDto:
    puuid: str
    gameName: str
    tagLine: str

@dataclass
class ActiveShardDto:
    puuid: str
    game: str
    activeShard: str