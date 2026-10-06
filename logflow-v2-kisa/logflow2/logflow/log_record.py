from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class LogRecord:
    """Degismez alan kaydi. `attributes` genisleme noktasidir: sonraki asamalar
    (5-7. hafta) ayristiricinin bilmedigi veriyi, yeni alan eklemeden kayda tasir."""

    timestamp: datetime
    client_ip: str
    method: str
    path: str
    status: int
    bytes: int
    user_agent: str
    attributes: Mapping[str, str] = field(default_factory=dict)
    raw: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))
