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

        if user_dto.role_id == 1:
            raise ValueError(
                "Sorry the admin role can't be added to user table")
        if user_dto.role_id == 2:
            self.insert_record.add_record("users", ["first_name", "last_name", "email", "password", "role_id"], [
                                          user_dto.first_name, user_dto.last_name, user_dto.email, user_dto.password, user_dto.role_id])

   
    def get_user_by_email_password(self, dto: GetUserDTO) -> UserDTO:

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
        try:
            self.db_connect.cursor.execute(
                "SELECT COUNT(*) FROM users WHERE email=%s;", (email,))
            cnt = self.db_connect.cursor.fetchone()[0]
            if cnt > 0:
                print("This email exist")
        except Exception as e:
            print("Error checking email", e)

    def add_like(self, like_dto: LikeDTO):
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

        try:
            self.db_connect.cursor.execute(
                "SELECT id, id_country, vacation_description, start_date, end_date, file_image, price FROM vacations ORDER BY start_date ASC;")
            row = self.db_connect.cursor.fetchall()
            return [
                VacationDTO(
                    id=row[0],
                    id_country=row[1],
                    vacation_description=[2],
                    start_date=row[3],
                    end_date=row[4],
                    file_image=row[5],
                    price=row[6]

                )
                for rows in row
            ]
        except Exception as e:
            print(f"Error getting vacations: {e}")
            return []

    def add_vacation(self, vacation_dto: VacationDTO):
        try:
            self.insert_record.add_record("vacations",
                                          ["country_id", "description", "start_date",
                                              "end_date", "file_img", "price"],
                                          [vacation_dto.country_id, vacation_dto.vacation_description, vacation_dto.start_date,
                                              vacation_dto.end_date, vacation_dto.file_img, vacation_dto.price])
        except Exception as e:
            print("Error adding vacation:", e)

    def del_vacation_by_id(self, id):
        try:
            self.delete_vacation.delete_row_by_parameters(
                "vacations", [("id", id)])
            
        except Exception as e:
            print("Error deleting vacation:", e)
    
    def get_vacation_by_id(self, id):
        try:
            self.get_row_by_id.get_row_by_id("vacations",id)
            return self.db_connect.cursor.fetchone()
        except Exception as e:
            print("Error getting vacation:", e)

        
