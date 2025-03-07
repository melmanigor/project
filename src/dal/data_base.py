import psycopg as pg

class Vacation_db_connect:
        
        def __init__(self,host,dbname,user,password):
            self.host=host
            self.dbname=dbname
            self.user=user
            self.password=password
            self.conn=None
            self.cursor=None
            self.connect()

        def connect(self):
            """
                Establishes a connection to the PostgreSQL database.

                Returns:
                        - None

            """
            self.conn=pg.connect(
                  host=self.host,
                  dbname=self.dbname,
                  user=self.user,
                  password=self.password
                )
            self.cursor=self.conn.cursor()

     
        