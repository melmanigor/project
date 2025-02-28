from src.dto.role_enum import Role

from dataclasses import dataclass

@dataclass
class UserDTO:
    user_id: int
    first_name:str
    last_name:str
    email:str
    role_id:Role
    password:str