from src.user_repository import User_repository
from src.dto.role_enum import Role
from src.dto.user_dto import UserDTO,GetUserDTO
from src.dto.like_dto import LikeDTO
import re


class UserFacade:

    def __init__(self, user_repo: User_repository):
        self.user_repo = user_repo

    def check_email(self, email: str) -> bool:
        """
        Validates whether the given email address is in a proper format.

         Args:
             email (str): The email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        valid_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(valid_email, email) is not None

    def user_registration(self, first_name: str, last_name: str, email: str, password: str, role: Role = Role.User):
        
        """"
        Adding  a new user in the system not ADMIN.

        Parameters:
              - first_name (str): The first name of the user.
              - last_name (str): The last name of the user.
              - email (str): The email address of the user.
              - password (str): The password for the user account (must be at least 4 characters long).
              - role (Role, optional): The role of the user (defaults to Role.User). Admin registration is not allowed.

        Raises:
             - ValueError: If the email format is invalid.
             - ValueError: If the password is less than 4 characters.
             - ValueError: If the email already exists in the system.
             - ValueError: If attempting to register an Admin.

        Returns:
            - str: A success message upon successful registration.
        """
        if not self.check_email(email):
                raise ValueError("Invalid email format")
        
        if len(password) < 4:
                raise ValueError("Password should be more then 4 digits")
            
        if self.user_repo.check_email_existences(email):
                raise ValueError("Email already exist")
            
        if role == Role.Admin:
                raise ValueError("Admin can't be registered")
            
        role_id=role.value
        new_user = UserDTO(user_id=None,first_name=first_name, last_name=last_name, email=email, password=password, role_id=role_id)
        self.user_repo.ad_user(new_user)
        return "User registered successfully" 
        

    def login(self, email: str, password: str):
        """"
        Log in of existed user   based on their email and password.

        Parameters:
            - email (str): The email address of the user.
            - password (str): The password associated with the user account (must be at least 4 characters long).

        Raises:
            - ValueError: If the email format is invalid.
            - ValueError: If the password is less than 4 characters.
            - ValueError: If the email or password is incorrect.

        Returns:
           - UserDTO: The authenticated user object if login is successful.

        """

        if not self.check_email(email):
            raise ValueError("Invalid email Format")
        if len(password) < 4:
            raise ValueError("Password should be more then 4 digits")
        email_password=GetUserDTO(email,password)
        user = self.user_repo.get_user_by_email_password(email_password)
        if user:
            print("User login successfully:", user)
            return user
        else:
            raise ValueError("Wrong password or email")

    def add_like_by_user(self, user_id: int, vacation_id: int):
        """"
         Adds a like to a vacation by a specific user.

         Parameters:
             - user_id (int): The ID of the user who is liking the vacation.
             - vacation_id (int): The ID of the vacation being liked.

        Returns
            - bool: True if the like was successfully added, False otherwis
        """
       
        like_dto = LikeDTO(user_id, vacation_id)
        return self.user_repo.add_like(like_dto)

    def delete_like_by_user(self, user_id: int, vacation_id: int):
        """"
        Removes a like from a vacation by a specific user.

        Parameters:
          - user_id (int): The ID of the user who wants to remove their like.
          - vacation_id (int): The ID of the vacation from which the like is being removed.

        Returns:
         - bool: True if the like was successfully removed, False otherwise.
        """
        delete_like = LikeDTO(user_id, vacation_id)
        return self.user_repo.remove_like(delete_like)
