import psycopg as pg

class Get_row_by_id:
     
    def __init__(self,db_connect):
         self.db_connect=db_connect

    def get_row_by_id(self, table:str,id:int):
         """
         Retrieves a row from the specified database table using its ID.

         Parameters:
                 - table (str): The name of the table from which the row should be retrieved.
                 - id (int): The ID of the record to be fetched.

         Returns:
                - tuple: The row data if found.
                - None: If no record is found.

        Exceptions:
                - Prints an error message if an exception occurs during execution.
         """
         
         
         try:
             self.db_connect.cursor.execute(f"SELECT * FROM {table} WHERE id=%s;",(id,))
             rows=self.db_connect.cursor.fetchone()
             if rows==None:
                 print(f"Error: No record found with ID {id} in table {table}.")
             else:
                return rows
             
         except Exception as e:
             print(e)
          
    
