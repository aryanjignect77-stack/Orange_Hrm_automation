from dataclasses import dataclass

@dataclass
class SystemUser:
    user_role: str
    employee_name: str
    username: str
    status: str
    password: str