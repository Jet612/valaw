from dataclasses import dataclass
from typing import Optional

@dataclass
class AccountDto:
    puuid: str
    gameName: Optional[str] = None
    tagLine: Optional[str] = None

@dataclass
class ActiveShardDto:
    puuid: str
    game: str
    activeShard: str