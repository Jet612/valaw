from dataclasses import dataclass


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
    type: str
    localizedNames: LocalizedNamesDto | None = None
    parentId: str | None = None


@dataclass
class ContentItemDto:
    name: str
    id: str
    assetName: str
    localizedNames: LocalizedNamesDto | None = None
    assetPath: str | None = None


@dataclass
class ContentDto:
    version: str
    characters: list[ContentItemDto]
    maps: list[ContentItemDto]
    chromas: list[ContentItemDto]
    skins: list[ContentItemDto]
    skinLevels: list[ContentItemDto]
    equips: list[ContentItemDto]
    gameModes: list[ContentItemDto]
    totems: list[ContentItemDto]
    sprays: list[ContentItemDto]
    sprayLevels: list[ContentItemDto]
    charms: list[ContentItemDto]
    charmLevels: list[ContentItemDto]
    playerCards: list[ContentItemDto]
    playerTitles: list[ContentItemDto]
    acts: list[ActDto]
    ceremonies: list[ContentItemDto]
