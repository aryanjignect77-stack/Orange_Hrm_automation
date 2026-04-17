from dataclasses import dataclass
from typing import Optional

@dataclass
class Language:
    language: Optional[str] = None
    fluency: Optional[str] = None
    competency: Optional[str] = None