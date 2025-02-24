from src.dal.data_base import Vacation_db_connect
from src.dal.insert_new_record import Insert_new_record

import psycopg as pg

class User_repository:
    
    def __init__(self,db_connect:Vacation_db_connect):
        self.db_connect=db_connect
        self.insert_record=Insert_new_record(db_connect)

    def ad_user(self,first_name,last_name,email,password,role_id):
        if role_id==1:
            raise ValueError("Sorry the admin role can't be added to user table")
        self.insert_record.add_record("users",["first_name","last_name","email","password","role_id"],[first_name,last_name,email,password,role_id])

    

