import unittest
import psycopg as pg



from src.dto.user_dto import UserDTO
from src.buisnes_logic.user_facade import UserFacade
from src.user_repository import User_repository
from test2.test_db_connect import Test_db_connect




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

        cls.db.cursor.execute("""
                              CREATE TABLE IF NOT EXISTS roles(
                               id SERIAL PRIMARY KEY,
                              role_name VARCHAR(20) NOT NULL UNIQUE);
                           
                              """)
        
        cls.db.cursor.execute("""
                              CREATE TABLE IF NOT EXISTS users(
                              id SERIAL PRIMARY KEY, 
                              first_name VARCHAR(20),
                              last_name VARCHAR(20),
                              email  VARCHAR(30) NOT NULL UNIQUE,
                              password VARCHAR(50),
                              role_id INT NOT NULL,
                             FOREIGN KEY (role_id) REFERENCES roles(id)ON DELETE CASCADE);
                              """)
       
        cls.db.cursor.execute("""
                               CREATE TABLE IF NOT EXISTS country(
                              id SERIAL PRIMARY KEY,country_name VARCHAR(30));
                               """)
       
        cls.db.cursor.execute("""
                              CREATE TABLE IF NOT EXISTS vacation(
                              id SERIAL PRIMARY KEY,
                              country_id SERIAL,
                              description TEXT,
                              start_date DATE,
                              end_date DATE,
                              file_img VARCHAR(255),
                              price FLOAT NOT NULL
                              FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE);

                              """)
        cls.db.cursor.execute("""CREATE TABLE IF NOT EXISTS likes(
                              user_id INT NOT NULL,
                              vacation_id SERIAL,
                              FOREIGN KEY(vacation_id) REFERENCES vacation(id) ON DELETE CASCADE,
                              FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);

                              """)
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
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()