from src.dal.data_base import Vacation_db_connect
from src.dal.insert_new_record import Insert_new_record
from src.dal.delete_row_by_id import DELETE_row_by_id
from src.dto.user_dto import UserDTO
from src.dto.role_enum import Role
from src.dto.like_dto import LikeDTO
import psycopg as pg

class User_repository:
    
    def __init__(self,db_connect:Vacation_db_connect):
        self.db_connect=db_connect
        self.insert_record=Insert_new_record(db_connect)
        self.delete_like=DELETE_row_by_id(db_connect)

    def ad_user(self,user_dto:UserDTO):

        if user_dto.role_id==1:
            raise ValueError("Sorry the admin role can't be added to user table")
        self.insert_record.add_record("users",["first_name","last_name","email","password","role_id"],[user_dto.first_name,user_dto.last_name,user_dto.email,user_dto.password,user_dto.role_id.value])

    def get_user_by_email_password(self,email,password):

        try:
            self.db_connect.cursor.execute("SELECT id,role_id, CONCAT(first_name, ' ',last_name) FROM users WHERE email=%s AND password=%s;",(email,password))
            row=self.db_connect.cursor.fetchone()
            if row:
                print(row)
            else:
                print("Wrong password or email")
        except Exception as e:
            print("Error to get user",e)
    
    def check_email_existences(self,email):
        try:
            self.db_connect.cursor.execute("SELECT COUNT(*) FROM users WHERE email=%s;",(email,))
            cnt=self.db_connect.cursor.fetchone()[0]
            if cnt>0:
                print("This email exist")
        except Exception as e:
            print ("Error checking email",e)

    def add_like(self,like_dto:LikeDTO):
        try:
            self.db_connect.cursor.execute("SELECT COUNT(*) FROM likes WHERE user_id=%s AND vacation_id=%s;",(like_dto.user_id,like_dto.vacation_id))
            likes_cnt=self.db_connect.cursor.fetchone()[0]
            if likes_cnt:
                print("This user already like this vacation")
            if likes_cnt==0:
                self.insert_record.add_record("likes",["user_id","vacation_id"],[like_dto.user_id,like_dto.vacation_id])
        except Exception as e:
            print("Error to add like",e)

    def remove_like(self,like_dto:LikeDTO):
        try:
            self.db_connect.cursor.execute("SELECT user_id FROM likes WHERE user_id=%s AND vacation_id=%s;",(like_dto.user_id,like_dto.vacation_id))
            row=self.db_connect.cursor.fetchone()
            if not row :
                print("This user not liked this vacation")
            self.delete_like.delete_row_by_parameters("likes",[["user_id", like_dto.user_id], ["vacation_id", like_dto.vacation_id]])
        
        except Exception as e:
            print("Fail to remove likes",e) 
