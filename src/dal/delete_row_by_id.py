import psycopg as pg


class DELETE_row_by_id:

    def __init__(self, db_connect):
        self.db_connect = db_connect

    def delete_row_by_id(self, table, id):
        self.delete_row_by_parameters(table, ["id", id])

    def delete_row_by_parameters(self, table:str, params:list[tuple[str,any]]):
        """
        Deletes a row from the specified database table based on given parameters.

        Parameters:
            - table (str): The name of the table from which the row should be deleted.
            - params (list[tuple[str, any]]): A list of tuples where each tuple contains:
            - The column name (str).
            - The corresponding value to match for deletion.

        Exceptions:
            - Raises ValueError if no record is found with the given parameters.
            - Prints an error message if any exception occurs during execution.

        Returns:
            - None

        """

        try:
           
            query_select = f"SELECT * FROM {table} WHERE "
            query_delete = f"DELETE FROM {table} WHERE "
            for i in range(len(params)):
                query_select += f"{params[i][0]} = %s"
                query_delete += f"{params[i][0]} = %s"
                if i < len(params)-1:
                    query_select += " AND "
                    query_delete += " AND "
                else:
                    query_select += ";"
                    query_delete += ";"
            self.db_connect.cursor.execute(
                query_select, [p[1] for p in params])
            row = self.db_connect.cursor.fetchone()
            if row is None:
                raise ValueError(
                    f"Error: No record found with params in table {table}.")
            self.db_connect.cursor.execute(
                query_delete, [p[1] for p in params])
            self.db_connect.conn.commit()
        except Exception as e:
            print(e)
