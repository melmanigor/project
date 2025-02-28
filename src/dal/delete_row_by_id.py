import psycopg as pg


class DELETE_row_by_id:

    def __init__(self, db_connect):
        self.db_connect = db_connect

    def delete_row_by_id(self, table, id):
        self.delete_row_by_parameters(table, ["id", id])

    def delete_row_by_parameters(self, table, params):
        try:
           # Check if the record exists first
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
