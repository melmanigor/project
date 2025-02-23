import psycopg as pg

class DELETE_row_by_id:
     
    def __init__(self,db_connect):
         self.db_connect=db_connect

    def delete_row_by_id(self, table,id):
             try:
            # Check if the record exists first
                self.db_connect.cursor.execute(f"SELECT * FROM {table} WHERE ID = %s;", (id,))
                row = self.db_connect.cursor.fetchone()
                if row is None:
                      raise ValueError(f"Error: No record found with ID {id} in table {table}.")
                self.db_connect.cursor.execute(f"DELETE  FROM {table} WHERE id=%s;",(id,))
                self.db_connect.conn.commit()
             except Exception as e:
                  print(e)

           