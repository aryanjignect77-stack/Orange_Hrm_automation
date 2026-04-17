from dataclasses import dataclass
from typing import Optional

@dataclass
class License:
    license_number: str
    issued_date: str
    expiry_date: str
    license_type: Optional[str] = None