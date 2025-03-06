from src.dto.role_enum import Role

from dataclasses import dataclass

@dataclass
class UserDTO:
    user_id: int
    first_name:str
    last_name:str
    email:str
    password:str
    role_id:int
@dataclass
class GetUserDTO:
        email:str
        password:str