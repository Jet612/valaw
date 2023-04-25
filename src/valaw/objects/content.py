from dataclasses import dataclass
from typing import List, Optional 

@dataclass
class LocalizedNamesDto:
    ar_AE: str
    de_DE: str
    en_GB: str
    en_US: str
    es_ES: str
    es_MX: str
    fr_FR: str
    id_ID: str
    it_IT: str
    ja_JP: str
    ko_KR: str
    pl_PL: str
    pt_BR: str
    ru_RU: str
    th_TH: str
    tr_TR: str
    vi_VN: str
    zh_CN: str
    zh_TW: str

@dataclass
class ActDto:
    name: str
    id: str
    isActive: bool
    localizedNames: Optional[LocalizedNamesDto] = None

@dataclass
class ContentItemDto:
    name: str
    id: str
    assetName: str
    localizedNames: Optional[LocalizedNamesDto] = None
    assetPath: Optional[str] = None

@dataclass
class ContentDto:
    version: str
    characters: List[ContentItemDto]
    maps: List[ContentItemDto]
    chromas: List[ContentItemDto]
    skins: List[ContentItemDto]
    skinLevels: List[ContentItemDto]
    equips: List[ContentItemDto]
    gameModes: List[ContentItemDto]
    sprays: List[ContentItemDto]
    sprayLevels: List[ContentItemDto]
    charms: List[ContentItemDto]
    charmLevels: List[ContentItemDto]
    playerCards: List[ContentItemDto]
    playerTitles: List[ContentItemDto]
    acts: List[ActDto]