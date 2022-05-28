import pytest
from database import Database

# todo: creation + dropping
# todo: reading
# todo: insertion

_test_cases_create = [
    ({'name': 'sentences', 'columns&types': (('id', 'INT'), ('sentence', 'TEXT')),
      'autoincrement': True, 'drop': False},
        """CREATE TABLE sentences
(id INT PRIMARY KEY AUTOINCREMENT,
sentence TEXT)"""),
    ({'name': 'word_forms', 'columns&types': (('id', 'INT'), ('sentence_id', 'INT'), ('word_form', 'TEXT'),
                                              ('pos', 'TEXT'), ('abs_freq', 'INT')),
      'autoincrement': True, 'drop': False},
        """CREATE TABLE word_forms
(id INT PRIMARY KEY AUTOINCREMENT,
sentence_id INT,
word_form TEXT,
pos TEXT,
abs_freq INT)""")
]


@pytest.mark.parametrize("test_case", _test_cases_create)
def test_create_table(test_case):
    db = Database('pos_statistics.db')
    name = test_case[0]['name']
    columns = test_case[0]['columns&types']
    autoincrement = test_case[0]['autoincrement']
    drop = test_case[0]['drop']
    creation_query = db.create_table(name, columns, autoincrement, drop)
    assert test_case[1] == creation_query


_test_cases_read = [
    ({'name': 'sentences', 'columns': '', 'where': "pos = 'NOUN'", 'num': 20, 'order_by': 'word_usage'},
     """""SELECT * FROM sentences
WHERE pos = 'NOUN'
LIMIT 20
ORDER BY word_usage"""),
    ({'name': 'sentences', 'columns': ('id', 'word_usage', 'pos'), 'where': "pos = 'NOUN'", 'num': 0, 'order_by': ''},
     """""SELECT (id, word_usage, pos) FROM sentences
WHERE pos = 'NOUN'""")
]


@pytest.mark.parametrize("test_case", _test_cases_read)
def test_read_from_table(test_case):
    db = Database('pos_statistics.db')
    name = test_case[0]['name']
    columns = test_case[0]['columns']
    where = test_case[0]['where']
    num = test_case[0]['num']
    order_by = test_case[0]['order_by']
    reading_query = db.read_from_table(name, columns, where, num, order_by)
    assert test_case[1] == reading_query


if __name__ == '__main__':
    # test_create_table()
    test_read_from_table()
