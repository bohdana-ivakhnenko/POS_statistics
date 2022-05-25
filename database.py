import sqlite3


def commit(db_function, self):
    def db_decorator(function):
        function()
        self.conn.commit()
    return db_decorator(db_function)


class Database:
    def __init__(self, name: str):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.c = self.conn.cursor()

    def close(self):
        self.conn.close()

    def create_table(self, table_name: str, columns: dict, autoincrement=True, drop=False) -> str:
        if drop:
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            self.c.execute(drop_query)

        auto = {True: " AUTOINCREMENT",
                False: ""}

        query = f"CREATE TABLE {table_name}\n"
        first_col = f"({columns[0][0]} {columns[0][1]} PRIMARY KEY{auto[autoincrement]},\n"
        cols = "\n".join([f"{column[0]} {column[1]}," for column in columns[1:]])
        query = query + first_col + cols.strip(' ,') + ")"

        self.c.execute(query)
        return query

    def read_from_table(self, name: str, columns: tuple, where, num, order_by, desc=True) -> str:
        if columns:
            columns = f"({' ,'.join(columns).strip(' ,')})"
        else:
            columns = "*"

        query = f"SELECT {columns} FROM {name}"

        if where:
            query = query + f" WHERE {where}"

        if order_by:
            order = {True: " DESC",
                    False: ""}
            query = query + f" ORDER BY {order_by}{order[desc]}"

        if num:
            query = query + f" LIMIT {num}"

        self.c.execute(query)
        return query

    def insert_into_table(self):
        pass
