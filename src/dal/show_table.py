import psycopg as pg

class Show_table:

    def __init__(self,db_connect):
          
          self.db_connect=db_connect

    def get_table(self,table):
             """
             Retrieves all rows from the specified database table.

             Parameters:
                 - table (str): The name of the table to fetch data from.

             Returns:
                    - List[Tuple[Any, ...]]: A list of tuples where each tuple represents a row from the table.
             Exceptions:
    -               - Prints an error message if an exception occurs during execution.
             """
             self.db_connect.cursor.execute(f"SELECT * FROM {table};")
             rows=self.db_connect.cursor.fetchall()
             for i in rows:
                  print(i)
