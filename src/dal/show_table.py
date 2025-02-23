import psycopg as pg

class Show_table:

    def __init__(self,db_connect):
          
          self.db_connect=db_connect

    def get_table(self,table):
             self.db_connect.cursor.execute(f"SELECT * FROM {table};")
             rows=self.db_connect.cursor.fetchall()
             for i in rows:
                  print(i)
