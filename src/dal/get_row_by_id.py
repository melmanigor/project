import psycopg as pg

class Get_row_by_id:
     
    def __init__(self,db_connect):
         self.db_connect=db_connect

    def get_row_by_id(self, table,id):
         try:
             self.db_connect.cursor.execute(f"SELECT * FROM {table} WHERE id=%s;",(id,))
             rows=self.db_connect.cursor.fetchone()
             if rows==None:
                 print(f"Error: No record found with ID {id} in table {table}.")
             else:
                for i in rows:
                  print(rows)
             
         except Exception as e:
             print(e)
          
    
