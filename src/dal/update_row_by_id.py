import psycopg as pg

class Update_table:

    def __init__(self,db_connect):
        self.db_connect=db_connect

    
    def update_row_by_id(self, table:str,column:str,new_value:any,id:int):
        """
        Updates a specific column of a row in a database table by its ID.

        Parameters:
                - table (str): The name of the table where the update should occur.
                - column (str): The name of the column to be updated.
                - new_value (Any): The new value to set for the specified column.
                - id (int): The ID of the record to be updated.

        Returns:
                - None

        Exceptions:
                - Raises ValueError if no record is found with the given ID.
                - Prints an error message if any exception occurs during execution.
        """
        try:
            self.db_connect.cursor.execute(f"SELECT * FROM {table} WHERE ID = %s;", (id,))
            row = self.db_connect.cursor.fetchone()
            if row is None:
                raise ValueError(f"Error: No record found with ID {id} in table {table}.")
            self.db_connect.cursor.execute(f"UPDATE {table} SET {column}=%s WHERE id=%s",(new_value,id))
            self.db_connect.conn.commit()
        
        except Exception as e:
            print(e)

