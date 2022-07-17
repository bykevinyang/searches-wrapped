from dataclasses import dataclass
from datetime import datetime

@dataclass
class search:
    title: str
    domain: str
    url: str
    time: datetime
    duration: datetime = None

    def __hash__(self):
        return hash(f"{self.time}")