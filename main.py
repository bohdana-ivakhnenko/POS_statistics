import processing, database


def create_a_table(type_text: str, type_table: str, columns, num_of_sub, data, auto_num):
    table_name = f"{type_table}_{type_text}"
    columns = columns + tuple([(str(num), 'INT') for num in range(1, num_of_sub+1)])
    db.create_table(table_name, columns, autoincrement=auto_num)
    db.insert_into_table(table_name, data)


def create_tables(data_type: str, db, word_forms=True, lemmas=True, pos=True, auto_num=False):
    with open(f"tales_{data_type}.txt", "r", encoding="utf-8") as file:
        text = file.read()

    if word_forms:
        word_forms_subs = processing.into_subsamples(text)
        num_of_sub = len(word_forms_subs)
        print("SUBSAMPLES IN", data_type, '\t', num_of_sub)

        word_forms_data = processing.into_word_forms_table(word_forms_subs)
        columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'word_forms', columns, num_of_sub, word_forms_data, auto_num)
    else:
        word_forms_data = db.read_from_table(f"word_forms_{data_type}")
        num_of_sub = len(word_forms_data[0]) - 5
    print("Finished on WORD FORMS")

    if lemmas:
        lemmas_data = processing.into_lemmas_table(word_forms_data)
        columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'lemmas', columns, num_of_sub, lemmas_data, auto_num)
    else:
        lemmas_data = db.read_from_table(f"lemmas_{data_type}")
    print("Finished on LEMMAS")

    if pos:
        pos_data = processing.into_pos_table(lemmas_data)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'pos', columns, num_of_sub, pos_data, auto_num)
    print("Finished on POS")


if __name__ == '__main__':
    db = database.Database("tales.db")
    types_of_tales = ("authors", "folk")

    for type_ in types_of_tales:
        create_tables(type_, db, auto_num=False)
