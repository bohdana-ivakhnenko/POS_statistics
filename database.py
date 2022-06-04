import sqlite3


def organize_values(line) -> str:
    """
    Перетворює список значень на перелік у стрічці, ставлячи стрічкові значення у лапки.
    :param line: список значень
    :return: список у стрічці типу "'a', 0, 1, 'м''яч'"
    """
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
        """
        Автоматично конструює SQL-запит для створення таблиці та виконує його.
        :param table_name: назва таблиці
        :param columns: список назв атрибутів (стовпчиків)
        :param autoincrement: якщо True, то перший атрибут - id, буде створено автоматично
        :param drop: якщо True, то перед створенням таблиця буде видалено
        :return: створений SQL-запит
        """
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

    def read_from_table(self, name: str, columns=(), where="", num=0, order_by="", desc=True, return_description=False,
                        print_query=True) -> tuple:
        """
        Автоматично створює SQL-запит для читання записів у таблиці.
        :param name: назва таблиці
        :param columns: список атрибутів (стовпчиків) у тій же послідовності, що й дані для них; якщо (), то зчитає всі
        :param where: фільтр пошуку - додається до запиту напряму, без перетворень!
        :param num: кількість рядків, які будуть зчитані; якщо 0, то ліміту не буде
        :param order_by: назва атрибута (стовпчика), за яким буде відсортовано результати
        :param desc: напрямок сортування; якщо True, то за спаданням
        :param return_description: якщо True, то функція поверне не лише зчитані рядки, а й опис таблиці
        :param print_query: чи друкувати SQL-запит перед виконанням
        :return: список зчитаних рядків із таблиці;
                 якщо return_description True, то також і опис таблиці (другим елементом)
        """
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
        
        if print_query:
            print(query)
    
        exe = self.c.execute(query)
        data = tuple(exe.fetchall())

        if return_description:
            return data, tuple([column[0] for column in list(exe.description)])
        return data

    def insert_into_table(self, name: str, data, multiple_rows: bool):
        """
        Автоматично створює SQL-запит для додавання дани до таблиці і виконує його.
        :param name: назва таблиці
        :param data: дані, які необхідно додати (для цілого рядка)
        :param multiple_rows: якщо True, то дані не для одного рядка, а багатьох
        :return: створений SQL-запит
        """
        query = ""
        if multiple_rows:
            for row in data:
                query = f"INSERT INTO {name} VALUES "
                query += organize_values(row)
                self.c.execute(query)
                self.conn.commit()
        else:
            query = f"INSERT INTO {name} VALUES "
            query += organize_values(data)
            self.c.execute(query)
            self.conn.commit()
        return query

    def delete_table(self, table_name: str) -> None:
        """
        Автоматично створює SQL-запит для видалення таблиці та виконує його.
        :param table_name: назва таблиці
        :return: None
        """
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        self.c.execute(drop_query)
        self.conn.commit()
