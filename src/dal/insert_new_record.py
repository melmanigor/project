import psycopg as pg

class Insert_new_record:

    def __init__(self,db_connect):
         self.db_connect=db_connect
    
    def add_record(self, table:str, columns:list, values:list):
        """
        Inserts a new record into the specified database table.

        Parameters:
            - table (str): The name of the table where the record should be inserted.
            - columns (List[str]): A list of column names where values will be inserted.
            - values (List[Any]): A list of values corresponding to the specified columns.

        Returns:
             - None

        Exceptions:
         - Prints an error message if an exception occurs during execution.
        """
        
        try:
            self.db_connect.cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})",values)
            
            self.db_connect.conn.commit()
            print(f"Record added successfully to {table}.")
        except Exception as e:
            print("Error adding record:", e)

    