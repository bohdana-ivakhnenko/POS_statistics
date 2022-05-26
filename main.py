import processing, database


def create_a_table(type_text: str, type_table: str, columns, num_of_sub, data, auto_num):
    table_name = f"{type_table}_{type_text}"
    columns = columns + tuple([(str(num), 'INT') for num in range(1, num_of_sub+1)])
    db.create_table(table_name, columns, autoincrement=auto_num)
    db.insert_into_table(table_name, data)


def create_tables(data_types: tuple, db, sentences=True, word_forms=True, lemmas=True, pos=True, auto_num=False):
    for type_ in data_types:
        with open(f"tales_{type_}.txt", "r", encoding="utf-8") as file:
            text = file.read()

        if sentences:
            sentences_data = processing.into_sentences_table(text, auto_num)
            columns = (('id', 'INT'), ('sentence', 'TEXT'))
            create_a_table(type_, 'sentences', columns, num_of_sub=0, data=sentences_data, auto_num=auto_num)
        else:
            sentences_data = db.read_from_table(f"sentences_{type_}")
        print("Finished on SENTENCES")

        if word_forms:
            word_forms_subs = processing.into_subsamples(sentences_data)
            num_of_sub = len(word_forms_subs)

            word_forms_data = processing.into_word_forms_table(word_forms_subs)
            columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
            create_a_table(type_, 'word_forms', columns, num_of_sub, word_forms_data, auto_num)
        else:
            word_forms_data = db.read_from_table(f"word_forms_{type_}")
            num_of_sub = len(word_forms_data[0]) - 5
        print("Finished on WORD FORMS")

        if lemmas:
            lemmas_data = processing.into_lemmas_table(word_forms_data)
            columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
            create_a_table(type_, 'lemmas', columns, num_of_sub, lemmas_data, auto_num)
        else:
            lemmas_data = db.read_from_table(f"lemmas_{type_}")
        print("Finished on LEMMAS")

        if pos:
            pos_data = processing.into_pos_table(lemmas_data)
            columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
            create_a_table(type_, 'pos', columns, num_of_sub, pos_data, auto_num)
        print("Finished on POS")


if __name__ == '__main__':
    db = database.Database("tales.db")
    types_of_tales = ("authors", "folk")
    create_tables(types_of_tales, db)
