from dataclasses import dataclass
from datetime import datetime


@dataclass
class search:
    title: str
    domain: str
    url: str
    time: datetime

    def __hash__(self):
        return hash(self.time)