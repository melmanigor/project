#from src.dal.data_base import Vacation_db_connect
from src.dal.show_table import Show_table
from src.dal.get_row_by_id import Get_row_by_id
from src.dal.delete_row_by_id import DELETE_row_by_id
#from src.dal.db_config import host,dbname,user,password
from src.dal.update_row_by_id import Update_table
from src.dal.insert_new_record import Insert_new_record
from src.user_repository import User_repository
from src.dto.like_dto import LikeDTO
from src.buisnes_logic.user_facade import UserFacade
from src.dto.role_enum import Role
from src.buisnes_logic.vacation_facade import VacationFacade
from test2.test_db_connect_config import host,user,password,dbname
from test2.test_db_connect import Test_db_connect
from datetime import date
import unittest
import psycopg as pg
# db=Vacation_db_connect(host=host, dbname=dbname, user=user, password=password)
# db.connect()
# cursor=db.cursor
# show=Show_table(db)
# show.get_table("vacation")
# show_id=Get_row_by_id(db)
# show_id.get_row_by_id("vacation",2)
# delete=DELETE_row_by_id(db)
# delete.delete_row_by_id("vacation",16)
# update=Update_table(db)
# update.update_row_by_id("vacation","price",5000,16)
# new_country=Insert_new_record(db)
# new_country.add_record("vacation",["start_date","end_date"],["01-12-2025","1-12-2026"])
# user=User_repository(db)
#user.ad_user("Izhak","Sade","izhaksade@gmail.com","54321",2)
#user.get_user_by_email_password("moshecohen@gmail.com",12345)
#user.check_email_existences("moshecohen@gmail.com")
#like=LikeDTO(2,5)
#user.add_like(like)
#user.remove_like(like)
# login=UserFacade(user)
# login.login("izhaksade@gmail.com","54321")
#add_like=UserFacade(user)
#add_like.add_like_by_user(2,5)
#add_like.delete_like_by_user(2,5)
# show_vacation=VacationFacade(user)
# vacations=show_vacation.get_all_vacation()
# for v in vacations:
#         print(v)
#show_vacation.ad_vacation(country_id=1,vacation_description="טיול חווייתי בפריז",start_date=date(2025, 7, 10),end_date=date(2025, 7, 20), file_img="paris_trip.jpg",price=2500)
# show_vacation.delete_vacation(15)
# cursor.close()
# db.conn.close()
class TestUserfacade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db=Test_db_connect(host=host,dbname=dbname,user=user,password=password)
        cls.db.connect()
        cls._setup_test_db()
        user_repo=User_repository(cls.db)
        cls.user_facade=UserFacade(user_repo)
    @classmethod
    def _setup_test_db(cls):
        cls.db.cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, role_id) 
            VALUES ('John', 'Doe', 'john@example.com', '1234', 2);
        """)
        cls.db.conn.commit()
    def test_login_success(self):
        email = "john@example.com"
        password = "1234"
        user=self.user_facade.login(email,password)
        self.assertIsNotNone(user)
   
    def test_login_fail(self):
        email = "john@example.com"
        password = "12345"
        user=self.user_facade.login(email,password)
        self.assertIsNone(user)
    
    def test_check_email_success(self):
        email = "john@example.com"
        email_check=self.user_facade.check_email(email)
        self.assertTrue(email_check,f"Valid email passed:{email}")

    def test_check_email_fail(self):
        email = "johnexample.com"
        email_check=self.user_facade.check_email(email)
        self.assertFalse(email_check,f"Invalid email passed:{email}")
 


if __name__ == "__main__":
    unittest.main()
