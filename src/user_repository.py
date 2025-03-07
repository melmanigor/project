from src.dal.data_base import Vacation_db_connect
from src.dal.insert_new_record import Insert_new_record
from src.dal.delete_row_by_id import DELETE_row_by_id
from src.dal.get_row_by_id import Get_row_by_id
from src.dal.show_table import Show_table
from src.dto.user_dto import UserDTO,GetUserDTO
from src.dto.role_enum import Role
from src.dto.like_dto import LikeDTO
from src.dto.vacation_dto import VacationDTO


import psycopg as pg


class User_repository:

    def __init__(self, db_connect: Vacation_db_connect):
        self.db_connect = db_connect
        self.insert_record = Insert_new_record(db_connect)
        self.delete_like = DELETE_row_by_id(db_connect)
        self.show_vacation = Show_table(db_connect)
        self.delete_vacation = DELETE_row_by_id(db_connect)
        self.get_row_by_id=Get_row_by_id(db_connect)

    def ad_user(self, user_dto: UserDTO):

        """"
        Adds a new user to the users table.

       Parameters:
         - user_dto (UserDTO): A data transfer object containing user details such as first name, last name, email, password, and role ID.

       Raises:
          - ValueError: If the user has an admin role (role_id == 1), as admin users cannot be added.

        Returns:
           - None
        
        """

        if user_dto.role_id == 1:
            raise ValueError(
                "Sorry the admin role can't be added to user table")
        if user_dto.role_id == 2:
            self.insert_record.add_record("users", ["first_name", "last_name", "email", "password", "role_id"], [
                                          user_dto.first_name, user_dto.last_name, user_dto.email, user_dto.password, user_dto.role_id])

   
    def get_user_by_email_password(self, dto: GetUserDTO) -> UserDTO:
        """"
        Retrieves a user from the database using their email and password.

        Parameters:
             - dto (GetUserDTO): A data transfer object containing the user's email and password.

         Returns:
             - UserDTO: A user object containing user details if found.
              - None: If no user is found with the given email and password.

        """

        self.db_connect.cursor.execute(
            "SELECT id, first_name,last_name,email,password,role_id FROM users WHERE email=%s AND password=%s;", (dto.email, dto.password))
        row = self.db_connect.cursor.fetchone()
        if row is None:
            print("No user is found")
            return None
        return UserDTO(

            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            password=row[4],
            role_id=Role(row[5])
        )

    def check_email_existences(self, email: str) -> bool:
        """"
        Checks if an email already exists in the users table.

        Parameters:
         - email (str): The email address to check.

        Returns:
         - bool: True if the email exists, False otherwise.

        Exceptions:
         - Prints an error message if an exception occurs during database execution.
        """
        try:
            self.db_connect.cursor.execute(
                "SELECT COUNT(*) FROM users WHERE email=%s;", (email,))
            cnt = self.db_connect.cursor.fetchone()[0]
            if cnt > 0:
                print("This email exist")
        except Exception as e:
            print("Error checking email", e)

    def add_like(self, like_dto: LikeDTO):
        """"
         Adds a like to a vacation by a user if the like does not already exist.

         Parameters:
                - like_dto (LikeDTO): A data transfer object containing user ID and vacation ID.

        Returns:
                - bool: True if the like was successfully added, False if the like already exists or an error occurs.

        Exceptions:
                - Prints an error message if an exception occurs during database execution.
        """
        try:
            self.db_connect.cursor.execute(
                "SELECT COUNT(*) FROM likes WHERE user_id=%s AND vacation_id=%s;", (like_dto.user_id, like_dto.vacation_id))
            likes_cnt = self.db_connect.cursor.fetchone()[0]
            if likes_cnt:
                print("This user already like this vacation")
                return False  # Did not add like
            if likes_cnt == 0:
                self.insert_record.add_record("likes", ["user_id", "vacation_id"], [
                                              like_dto.user_id, like_dto.vacation_id])
                return True
        except Exception as e:
            print("Error to add like", e)
            return False  # Did not add like

    def remove_like(self, like_dto: LikeDTO):
        """"
        Removes a like from a vacation by a user if it exists.

        Parameters:
             - like_dto (LikeDTO): A data transfer object containing user ID and vacation ID.

        Returns:
             - bool: True if the like was successfully removed, False if the like does not exist or an error occurs.

        Exceptions:
            - Prints an error message if an exception occurs during database execution.
        """
        try:
            self.db_connect.cursor.execute(
                "SELECT user_id FROM likes WHERE user_id=%s AND vacation_id=%s;", (like_dto.user_id, like_dto.vacation_id))
            row = self.db_connect.cursor.fetchone()
            if not row:
                print("This user not liked this vacation")
                return False
            self.delete_like.delete_row_by_parameters(
                "likes", [["user_id", like_dto.user_id], ["vacation_id", like_dto.vacation_id]])
            return True
        except Exception as e:
            print("Fail to remove likes", e)
            return False

    def get_all_vacations(self) -> list[VacationDTO]:
        """
        Retrieves all vacations from the database, ordered by start date.

        Returns:
            - list[VacationDTO]: A list of vacation objects containing vacation details.

        Exceptions:
          - Prints an error message if an exception occurs during database execution.
           - Returns an empty list if an error occurs.
        """

        try:
            self.db_connect.cursor.execute(
                "SELECT id, country_id, description, start_date, end_date, file_img, price FROM vacations ORDER BY start_date ASC;")
            row = self.db_connect.cursor.fetchall()
            return [
                VacationDTO(
                    id=vacation[0],
                    country_id=vacation[1],
                    description=vacation[2],
                    start_date=vacation[3],
                    end_date=vacation[4],
                    file_img=vacation[5],
                    price=vacation[6]

                )
                for vacation in row
            ]
        except Exception as e:
            print(f"Error getting vacations: {e}")
            return []

    def add_vacation(self, vacation_dto: VacationDTO):
        """
        Adds a new vacation to the vacations table in database.

       Parameters:
            - vacation_dto (VacationDTO): A data transfer object containing vacation details such as:
            - country_id (int): The ID of the country where the vacation takes place.
            - vacation_description (str): A description of the vacation.
            - start_date (str or datetime): The start date of the vacation.
            - end_date (str or datetime): The end date of the vacation.
            - file_img (str): The image file path or URL for the vacation.
            - price (float): The price of the vacation.

        Exceptions:
             - Prints an error message if an exception occurs during database execution.

        Returns:
                - None
        """
        try:
            self.insert_record.add_record("vacations",
                                          ["country_id", "description", "start_date",
                                              "end_date", "file_img", "price"],
                                          [vacation_dto.country_id, vacation_dto.vacation_description, vacation_dto.start_date,
                                              vacation_dto.end_date, vacation_dto.file_img, vacation_dto.price])
        except Exception as e:
            print("Error adding vacation:", e)

    def del_vacation_by_id(self, id:int):
        """
        Deletes a vacation from the database by its ID.

        Parameters:
            - id (int): The ID of the vacation to be deleted.

        Exceptions:
             - Prints an error message if an exception occurs during database execution.

        Returns:
             - None
        """
        try:
            self.delete_vacation.delete_row_by_parameters(
                "vacations", [("id", id)])
            
        except Exception as e:
            print("Error deleting vacation:", e)
    
    def get_vacation_by_id(self, id):
        """
        Retrieves a vacation from the database by its ID.

        Parameters:
             - id (int): The ID of the vacation to be retrieved.

        Returns:
            - VacationDTO: A vacation object if found.
            - None: If no vacation is found or an error occurs.

        Exceptions:
            - Prints an error message if an exception occurs during database execution.
        """

        try:
            self.get_row_by_id.get_row_by_id("vacations",id)
            return self.db_connect.cursor.fetchone()
        except Exception as e:
            print("Error getting vacation:", e)

        
