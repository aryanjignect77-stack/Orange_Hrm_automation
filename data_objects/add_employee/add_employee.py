from dataclasses import dataclass

@dataclass
class AddEmployee:
    first_name: str
    middle_name: str
    last_name: str
    employee_id: str

    username: str
    password: str
    confirm_password: str