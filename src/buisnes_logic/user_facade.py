from src.user_repository import User_repository
from src.dto.role_enum import Role
from src.dto.user_dto import UserDTO
from src.dto.like_dto import LikeDTO
import re

class UserFacade:

    def __init__(self,user_repo:User_repository):
        self.user_repo=user_repo
   
    def check_email(self,email:str)->bool:

        """
        Validates whether the given email address is in a proper format.

         Args:
             email (str): The email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        valid_email=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(valid_email,email) is not None
    
    def user_registration(self,first_name:str,last_name:str,email:str,password:str,role:Role=Role.User):
        if not self.check_email(email):
            raise ValueError("Invalid email format")
        if len(password)<4:
            raise ValueError("Password should be more then 4 digits")
        if self.user_repo.check_email_existences(email):
            raise ValueError("Email already exist")
        if role==Role.Admin:
            raise ValueError("Admin can't be registered")
        new_user=UserDTO(first_name,last_name,email,password,role)
        self.user_repo.ad_user(new_user)

    def login(self,email:str,password:str):
        if not self.check_email(email):
            raise ValueError("Invalid email Format")
        if len(password)<4:
            raise ValueError("Password should be more then 4 digits")
        user=self.user_repo.get_user_by_email_password(email,password)
        if user:
            print("User login successfully:",user)
            return user
        else:
            raise ValueError("Wrong password or email")
    
    def add_like_by_user(self,user_id:int,vacation_id:int):
        like_dto=LikeDTO(user_id,vacation_id)
        self.user_repo.add_like(like_dto)
    
    def delete_like_by_user(self,user_id:int,vacation_id:int):
        delete_like=LikeDTO(user_id,vacation_id)
        self.user_repo.remove_like(delete_like)

        