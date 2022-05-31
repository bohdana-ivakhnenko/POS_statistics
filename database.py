import sqlite3


def organize_values(line) -> str:
    values = ""
    for value in line:
        if type(value) == int:
            values += f", {value}"
        elif type(value) == str:
            value = value.replace("'", "''")
            values += f", '{value}'"
        else:
            print("Something is wrong with organizing:", line)
    return f"({values.strip(', ')})"


class Database:
    def __init__(self, name: str):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.c = self.conn.cursor()

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

    def read_from_table(self, name: str, columns=(), where="", num=0, order_by="", desc=True) -> tuple:
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

        print(query)
        data = tuple(self.c.execute(query).fetchall())
        return data

    def insert_into_table(self, name: str, data, multiple_rows: bool):
        query = ""
        if multiple_rows:
            for row in data:
                query = f"INSERT INTO {name} VALUES "
                query += organize_values(row)
                # print("insert", query)
                self.c.execute(query)
                self.conn.commit()
        else:
            query = f"INSERT INTO {name} VALUES "
            query += organize_values(data)
            self.c.execute(query)
            self.conn.commit()
        return query

    def delete_table(self, table_name: str) -> None:
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        self.c.execute(drop_query)
        self.conn.commit()
