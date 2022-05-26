import sqlite3


class Database:
    def __init__(self, name: str):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.c = self.conn.cursor()

    def delete_table(self, table_name: str) -> None:
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        self.c.execute(drop_query)

    def create_table(self, table_name: str, columns: tuple, autoincrement=True, drop=False) -> str:
        if drop:
            self.delete_table(table_name)

        auto = {True: " AUTOINCREMENT",
                False: ""}

        query = f"CREATE TABLE {table_name}\n"
        first_col = f"({columns[0][0]} {columns[0][1]} PRIMARY KEY{auto[autoincrement]},\n"
        cols = "\n".join([f"{column[0]} {column[1]}," for column in columns[1:]])
        query = query + first_col + cols.strip(' ,') + ")"

        self.c.execute(query)
        self.conn.commit()
        return query

    def read_from_table(self, name: str, columns: tuple, where: str, num: int, order_by: str, desc=True) -> str:
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

    def insert_into_table(self, name: str, data):
        query = f"INSERT INTO {name} VALUES "
        if type(data[0]) in {set, tuple, list}:
            for row in data:
                values = "', '".join(row)
                query = query + f"('{values}')"
                self.c.execute(query)
        else:
            values = "', '".join(data)
            query = query + f"('{values}')"
            self.c.execute(query)
        return query

