from dataclasses import dataclass
from datetime import datetime

@dataclass
class search:
    title: str
    domain: str
    url: str
    time: datetime
    duration: datetime = None

    def __str__(self):
        return f"{self.domain}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __hash__(self):
        return hash(f"{self.domain}")