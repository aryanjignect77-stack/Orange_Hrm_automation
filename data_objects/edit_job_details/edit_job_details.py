from dataclasses import dataclass
from typing import Optional

@dataclass
class EditJobDetails:
    joined_date: str
    job_title: Optional[str] = None
    job_category: Optional[str] = None
    sub_unit: Optional[str] = None
    location: Optional[str] = None
    employment_status: Optional[str] = None