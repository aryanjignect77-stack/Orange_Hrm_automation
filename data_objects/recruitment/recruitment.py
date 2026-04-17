from dataclasses import dataclass
from typing import Optional

@dataclass
class Recruitment:
    first_name: str
    middle_name: str
    last_name: str
    email: str
    contact_number: str
    keywords: str
    date_of_application: str
    notes: str

    vacancy: Optional[str] = None