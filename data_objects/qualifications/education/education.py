from dataclasses import dataclass
from typing import Optional

@dataclass
class Education:
    major_specialization: str
    institute: str
    year: str
    gpa_score: str
    start_date: str
    end_date: str
    level: Optional[str] = None