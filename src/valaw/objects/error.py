from dataclasses import dataclass

@dataclass
class statusDto:
    message: str
    status_code: int

@dataclass
class ErrorDto:
    status: statusDto