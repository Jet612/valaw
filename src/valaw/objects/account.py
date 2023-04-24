from dataclasses import dataclass

@dataclass
class AccountDto:
    puuid: str
    gameName: str
    tagLine: str