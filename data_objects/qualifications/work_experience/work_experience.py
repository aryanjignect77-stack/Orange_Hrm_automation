from dataclasses import dataclass
from datetime import date

@dataclass
class WorkExperience:
    company: str
    job_title: str
    from_date: date
    to_date: date
    comment: str