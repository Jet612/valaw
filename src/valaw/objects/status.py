from dataclasses import dataclass


@dataclass
class UpdateDto:
    id: int
    author: str
    publish: bool
    publish_locations: list[str]
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
    titles: list[ContentDto]
    updates: list[UpdateDto]
    created_at: str
    updated_at: str
    platforms: list[str]
    archived_at: str | None = None


@dataclass
class PlatformDataDto:
    id: str
    name: str
    locales: list[str]
    maintenances: list[StatusDto]
    incidents: list[StatusDto]
