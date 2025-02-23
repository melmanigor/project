import psycopg as pg

class Update_table:

    def __init__(self,db_connect):
        self.db_connect=db_connect

    
    def update_row_by_id(self, table,column,new_value,id):
        try:
            self.db_connect.cursor.execute(f"SELECT * FROM {table} WHERE ID = %s;", (id,))
            row = self.db_connect.cursor.fetchone()
            if row is None:
                raise ValueError(f"Error: No record found with ID {id} in table {table}.")
            self.db_connect.cursor.execute(f"UPDATE {table} SET {column}=%s WHERE id=%s",(new_value,id))
            self.db_connect.conn.commit()
        
        except Exception as e:
            print(e)

