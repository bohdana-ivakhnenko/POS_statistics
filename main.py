import processing, database


def create_tables(data_types: tuple, db, sentences=True, word_forms=True, lemmas=True, pos=True):
    for type_ in data_types:
        with open(f"tales_{type_}.txt", "r", encoding="utf-8") as file:
            text = file.read()

        if sentences:
            sentences_table = processing.into_sentences_table(text)
            db.create_table(f"sentences_{type_}", sentences_table, autoincrement=False)
        else:
            sentences_table = db.read_from_table(f"sentences_{type_}")
        print("Finished on SENTENCES")

        if word_forms:
            word_forms_table = processing.into_word_forms_table(sentences_table)
            db.create_table(f"word_forms_{type_}", word_forms_table, autoincrement=False)
        else:
            word_forms_table = db.read_from_table(f"word_forms_{type_}")
        print("Finished on WORD FORMS")

        if lemmas:
            lemmas_table = processing.into_lemmas_table(word_forms_table)
            db.create_table(f"lemmas_{type_}", lemmas_table, autoincrement=False)
        else:
            lemmas_table = db.read_from_table(f"lemmas_{type_}")
        print("Finished on LEMMAS")

        if pos:
            pos_table = processing.into_pos_table(lemmas_table)
            db.create_table(f"pos_{type_}", pos_table, autoincrement=False)
        print("Finished on POS")


if __name__ == '__main__':
    db = database.Database("tales.db")
    types_of_tales = ("authors", "folk")
    create_tables(types_of_tales, db)