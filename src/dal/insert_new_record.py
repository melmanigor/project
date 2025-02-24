import psycopg as pg

class Insert_new_record:

    def __init__(self,db_connect):
         self.db_connect=db_connect
    
    def add_record(self, table, columns, values):
        
        try:
            self.db_connect.cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})",values)
            
            self.db_connect.conn.commit()
            print(f"Record added successfully to {table}.")
        except Exception as e:
            print("Error adding record:", e)

    