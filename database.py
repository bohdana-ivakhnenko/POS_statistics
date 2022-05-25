import sqlite3


class Database:
    def __init__(self, name: str):
        self.name = name
        self.c = sqlite3.connect(self.name).cursor()

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

    def read_from_table(self, name, columns, where, num, order_by) -> str:
        query = ""
        return query

    def insert_into_table(self):
        pass
