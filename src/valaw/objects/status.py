from dataclasses import dataclass
from typing import List, Optional

@dataclass
class UpdateDto:
    id: int
    author: str
    publish: bool
    publish_locations: List[str]
    created_at: str
    updated_at: str

@dataclass
class ContentDto:
    locale: str
    content: str

@dataclass
class StatusDto:
    id: int
    maintenance_status: str
    incident_severity: str
    titles: List[ContentDto]
    updates: List[UpdateDto]
    created_at: str
    archived_at: str
    updated_at: str
    platforms: List[str]

@dataclass
class PlatformDataDto:
    id: str
    name: str
    locales: List[str]
    maintenances: List[StatusDto]
    incidents: List[StatusDto]