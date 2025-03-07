# from src.dal.data_base import Vacation_db_connect
from src.dal.show_table import Show_table
from src.dal.get_row_by_id import Get_row_by_id
from src.dal.delete_row_by_id import DELETE_row_by_id
from src.dal.db_config import host,dbname,user,password
from src.dal.update_row_by_id import Update_table
from src.dal.insert_new_record import Insert_new_record
from src.user_repository import User_repository
from src.dto.like_dto import LikeDTO
from src.buisnes_logic.user_facade import UserFacade
from src.dto.role_enum import Role
from src.buisnes_logic.vacation_facade import VacationFacade
from test2.test_db_connect_config import host, user, password, dbname
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
# new_country.add_record("vacation",["start_date","end_date"],["01-12-2025","1-12-2026"])\\
# user=User_repository(db)
# user.ad_user("Izhak","Sade","izhaksade@gmail.com","54321",2)
# user.get_user_by_email_password("moshecohen@gmail.com",12345)
# user.check_email_existences("moshecohen@gmail.com")
# like=LikeDTO(2,5)
# user.add_like(like)
# user.remove_like(like)
# login=UserFacade(user)
# login.login("izhaksade@gmail.com","54321")
# add_like=UserFacade(user)
# add_like.add_like_by_user(2,5)
# add_like.delete_like_by_user(2,5)
# show_vacation=VacationFacade(user)
# vacations=show_vacation.get_all_vacation()
# for vacation in vacations:
#             print(f"ID: {vacation.id}, Country ID: {vacation.country_id}, Description: {vacation.description}, "
#                   f"Start Date: {vacation.start_date}, End Date: {vacation.end_date}, Image: {vacation.file_img}, Price: {vacation.price}")
# show_vacation.ad_vacation(country_id=1,vacation_description="טיול חווייתי בפריז",start_date=date(2025, 7, 10),end_date=date(2025, 7, 20), file_img="paris_trip.jpg",price=2500)
# show_vacation.delete_vacation(15)
# cursor.close()
# db.conn.close()


    
class TestUserfacade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Test_db_connect(
            host=host, dbname=dbname, user=user, password=password)
        cls.db.connect()
        cls._setup_test_db()
        user_repo = User_repository(cls.db)
        cls.user_facade = UserFacade(user_repo)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    @classmethod
    def _setup_test_db(cls):
        cls.db.cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute(
            "TRUNCATE TABLE vacations RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, role_id) 
            VALUES ('John', 'Doe', 'john@example.com', '1234', 2);
        """)
        cls.db.cursor.execute("""
           INSERT into vacations (country_id, description, start_date, end_date, file_img, price) values(1, 'israel vacation', '01-01-2010', '01-01-2012', 'http://google.com/', 500);
        """)
        cls.db.conn.commit()

    def test_login_success(self):
        email = "john@example.com"
        password = "1234"
        user = self.user_facade.login(email, password)
        self.assertIsNotNone(user)

    def test_login_fail(self):
        email = "john@example.com"
        password = "1234555"
        with self.assertRaises(ValueError):
            user = self.user_facade.login(email, password)

    def test_check_email_success(self):
        email = "john@example.com"
        email_check = self.user_facade.check_email(email)
        self.assertTrue(email_check, f"Valid email passed:{email}")

    def test_check_email_fail(self):
        email = "johnexample.com"
        email_check = self.user_facade.check_email(email)
        self.assertFalse(email_check, f"Invalid email passed:{email}")

    def test_add_user_like(self):
        user_id = 1
        vacation_id = 1
        success = self.user_facade.add_like_by_user(user_id, vacation_id)
        self.assertTrue(
            success, f"Adding like from user {user_id} to vacation {vacation_id} failed..")

    def test_remove_user_like(self):
        user_id = 1
        vacation_id = 1
        success = self.user_facade.delete_like_by_user(user_id, vacation_id)
        self.assertTrue(
            success, f"Removing like from user {user_id} to vacation {vacation_id} failed..")

    def test_add_user_like_fail(self):
        user_id = 1
        vacation_id = 1
        success = self.user_facade.add_like_by_user(user_id, vacation_id)
        self.assertFalse(
            success, f"Adding like from user {user_id} to vacation {vacation_id} should have failed..")

    def test_remove_user_like_fail(self):
        user_id = 1
        vacation_id = 1
        success = self.user_facade.delete_like_by_user(user_id, vacation_id)
        self.assertFalse(
            success, f"Removing like from user {user_id} to vacation {vacation_id} should have failed..")
        
    def test_user_registration_susses(self):
        first_name="John"
        last_name="Doe"
        email="izhak@example.com"
        password="1234"
        role_id=Role.User

        success_user_reg=self.user_facade.user_registration(first_name,last_name,email,password,role_id)
        self.assertTrue(success_user_reg,f"Add user success")

    def test_user_registration_fail(self):
        first_name="izhak"
        last_name="Doe"
        email="izhak@example.com"
        password="1234"
        role_id=Role.Admin
        with self.assertRaises(ValueError) as context:
            self.user_facade.user_registration(first_name,last_name,email,password,role_id)
            
        error_message = str(context.exception)
        print( "Test Failed as Expected:", error_message) 
        self.assertEqual(error_message, "Admin can't be registered") 


class TestVacationFacade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Test_db_connect(
            host=host, dbname=dbname, user=user, password=password)
        cls.db.connect()
        cls._setup_test_db()
        user_repo = User_repository(cls.db)
        cls.vacation_facade = VacationFacade(user_repo)

    @classmethod
    def tearDownClass(cls):
            cls.db.close()


    @classmethod
    def _setup_test_db(cls):
        cls.db.cursor.execute("TRUNCATE TABLE vacations RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute(
            "TRUNCATE TABLE vacations RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute(
            "TRUNCATE TABLE country RESTART IDENTITY CASCADE;")
        cls.db.cursor.execute("""
            INSERT INTO country (country_name) 
            VALUES ('France'), ('Italy');
        """)
        cls.db.conn.commit()

    def test_add_vacation_success(self):
        response=self.vacation_facade.ad_vacation(country_id=1,vacation_description="Trip to paris",start_date=date(2025,10,6),end_date=date(2025,10,12),file_img="paris",price=2500)
        self.assertEqual(response, "Vacation added successfully")
    
    def test_add_vacation_fail(self):
        country_id=1
        vacation_description="Trip to paris"
        start_date=date(2025,10,6)
        end_date=date(2025,10,12)
        file_img="paris"
        price=-2500
        with self.assertRaises(ValueError) as context:
            self.vacation_facade.ad_vacation(country_id,vacation_description,start_date,end_date,file_img,price)
            
        error_message = str(context.exception)
        print( "Test Failed as Expected:", error_message) 
        self.assertEqual(error_message, "The price should be between 0 and 10000") 

    # def test_delete_vacation_fail(self):
    #     with self.assertRaises(ValueError) as context:
    #           self.vacation_facade.delete_vacation(2)
    #     error_message = str(context.exception) 
    #     print( "Test Failed as Expected:", error_message)
    #     self.assertEqual(error_message,"Vacation not found")


    def test_delete_vacation_success(self):
        response=self.vacation_facade.delete_vacation(1)
        print("Tests delete success")
        self.assertEqual(response, "Vacation DELETED")
        print("Test delete pass")
    
    


    

    
    
    
    

if __name__ == "__main__":
    unittest.main()