import processing
import database


def create_a_table(type_text: str, type_table: str, columns, num_of_sub, data, auto_num):
    table_name = f"{type_table}_{type_text}"
    columns = columns + tuple([(f"'{num}'", 'INT') for num in range(1, num_of_sub+1)])
    print(db.create_table(table_name, columns, autoincrement=auto_num, drop=True))
    db.insert_into_table(table_name, data, multiple_rows=True)


def create_tables(data_type: str, db, word_forms=False, lemmas=False, pos=False, auto_num=False, num_of_sub=0):
    with open(f"tales_{data_type}.txt", "r", encoding="utf-8") as file:
        text = file.read()

    if word_forms:
        print("START on WORD FORMS")
        word_forms_subs = processing.into_subsamples(text, num_of_sub)
        # num_of_sub = len(word_forms_subs)
        print("SUBSAMPLES IN", data_type, ':\t', num_of_sub)

        word_forms_data = processing.into_word_forms_table(word_forms_subs, auto_num=auto_num)
        columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'word_forms', columns, num_of_sub, word_forms_data, auto_num)
    elif lemmas:
        word_forms_data = db.read_from_table(f"word_forms_{data_type}")
        num_of_sub = len(word_forms_data[0]) - 5
    print("Finished on WORD FORMS")

    if lemmas:
        print("START on LEMMAS")
        lemmas_data = processing.into_lemmas_table(word_forms_data, auto_num=auto_num)
        columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'lemmas', columns, num_of_sub, lemmas_data, auto_num)
    elif pos:
        lemmas_data = db.read_from_table(f"lemmas_{data_type}")
    print("Finished on LEMMAS")

    if pos:
        print("START on POS")
        pos_data = processing.into_pos_table(lemmas_data, auto_num=auto_num)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'pos', columns, num_of_sub, pos_data, auto_num)
    print("Finished on POS")


if __name__ == '__main__':
    db = database.Database("tales.db")

    authors_tales = "authors"
    folk_tales = "folk"

    create_tables(authors_tales, db, num_of_sub=35, word_forms=False, lemmas=False, pos=False)
    create_tables(folk_tales, db, num_of_sub=35, word_forms=False, lemmas=False, pos=False)

    data = db.read_from_table("word_forms_folk", where="pos IN ('PUNCT', 'X')")
    print("num of word forms: ", len(data))
    [print(line) for line in data[:50]]

    data = db.read_from_table("lemmas_folk", order_by="abs_freq")
    print("num of lemmas: ", len(data))
    [print(line) for line in data[:50]]

    data = db.read_from_table("pos_folk", order_by="abs_freq")
    print("num of pos: ", len(data))
    [print(line) for line in data[:50]]

    db.conn.close()
