import processing
import database
from statistics import group, group_by_intervals, frequency_polygon, frequency_polygon_by_intervals, arithmetic_mean, \
    standard_error, frequency_fluctuations, coefficient_of_variation, relative_coefficient_of_variation, \
    relative_error, relative_subtraction, check_uniformity, students_criterion, freedom_greade, standard_deviation
import matplotlib as mpl


def create_a_table(type_text: str, type_table: str, columns, num_of_sub, data, auto_num):
    table_name = f"{type_table}_{type_text}"
    columns = columns + tuple([(f"'{num}'", 'INT') for num in range(1, num_of_sub+1)])
    print(db.create_table(table_name, columns, autoincrement=auto_num, drop=True))
    db.insert_into_table(table_name, data, multiple_rows=True)


def create_tables(data_type: str, db, num_of_sub=0,
                  word_forms=False, lemmas=False, pos=False, auto_num=False, pos_filter=False):
    with open(f"sources\\tales_{data_type}.txt", "r", encoding="utf-8") as file:
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
    elif pos or pos_filter:
        lemmas_data = db.read_from_table(f"lemmas_{data_type}")
    print("Finished on LEMMAS")

    if pos:
        print("START on POS")
        pos_data = processing.into_pos_table(lemmas_data, auto_num=auto_num)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'pos', columns, num_of_sub, pos_data, auto_num)

    if pos_filter:
        print("START on filtering POS")
        pos_filter_data = processing.into_pos_table(lemmas_data, auto_num=auto_num, filter_=True)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(data_type, 'pos_filtered', columns, num_of_sub, pos_filter_data, auto_num)
    print("Finished on POS")


def do_reading(type_: str, db, num_of_rows: int = -1, word_forms=False, lemmas=False, pos=False, pos_filter=False) -> None:
    if word_forms:
        data = db.read_from_table(f"word_forms_{type_}")
        print("num of word forms: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if lemmas:
        data = db.read_from_table(f"lemmas_{type_}", order_by="abs_freq")
        print("num of lemmas: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if pos:
        data = db.read_from_table(f"pos_{type_}", order_by="abs_freq")
        print("num of pos: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if pos_filter:
        data = db.read_from_table(f"pos_filtered_{type_}", order_by="abs_freq")
        print("num of pos filtered: ", len(data))
        [print(line) for line in data[:num_of_rows]]


def do_calculations(db, table="pos_filtered", polygons=True, order_by="pos", where=""):
    index = 3
    if table.startswith("word_form"):
        index = 5
    elif table.startswith("lemma"):
        index = 4
    elif table.startswith("pos"):
        index = 3

    authors_ = db.read_from_table(f"{table}_authors", order_by=order_by, where=where)
    folk_ = db.read_from_table(f"{table}_folk", order_by=order_by, where=where)

    for data_a, data_f in zip(authors_, folk_):
        subs_a = data_a[index:]
        subs_f = data_f[index:]

        grouped_a = group(subs_a)
        grouped_f = group(subs_f)

        grouped_intervals_a = group_by_intervals(subs_a)
        grouped_intervals_f = group_by_intervals(subs_f)

        mean_a = arithmetic_mean(grouped_a)
        mean_f = arithmetic_mean(grouped_f)

        st_dev_a = standard_deviation(grouped_a, mean_a)
        st_dev_f = standard_deviation(grouped_f, mean_f)

        st_err_a = standard_error(st_dev_a, len(subs_a), s=False)
        st_err_f = standard_error(st_dev_f, len(subs_f), s=False)

        stripes_a = frequency_fluctuations(mean_a, st_dev_a, visualise=False)
        stripes_f = frequency_fluctuations(mean_f, st_dev_f, visualise=False)

        coef_var_a = coefficient_of_variation(st_dev_a, mean_a)
        coef_var_f = coefficient_of_variation(st_dev_f, mean_f)

        rel_coef_var_a = relative_coefficient_of_variation(st_dev_a, mean_a, len(subs_a), data_a[2])
        rel_coef_var_f = relative_coefficient_of_variation(st_dev_f, mean_f, len(subs_f), data_f[2])

        rel_err_a = relative_error((st_err_a, mean_a))
        rel_err_f = relative_error((st_err_f, mean_f))

        # with open(f"results\\{data_a[1]}.txt", "w", encoding="utf-8") as file:
        #     print(f"Варіаційний ряд автори:", file=file)
        #     print(grouped_a, file=file, end='\n\n')
        #     print(f"Варіаційний ряд фольк:", file=file)
        #     print(grouped_f, file=file, end='\n\n')
        #
        #     print(f"Інтервальний ряд автори:", file=file)
        #     print(grouped_intervals_a, file=file, end='\n\n')
        #     print(f"Інтервальний ряд фольк:", file=file)
        #     print(grouped_intervals_f, file=file, end='\n\n')
        #
        #     print(f"Середнє арифметичне:\nавтори\tфольк", file=file)
        #     print(mean_a, mean_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Середнє квадратичне відхилення:\nавтори\tфольк", file=file)
        #     print(st_dev_a, st_dev_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Міра коливання середньої частоти:\nавтори\tфольк", file=file)
        #     print(st_err_a, st_err_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Смуги коливання:\nавтори\tфольк", file=file)
        #     print(stripes_a, stripes_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Коефіцієнт варіації - V (у відсотках):\nавтори\tфольк", file=file)
        #     print(coef_var_a, coef_var_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Коефіцієнт стабільности - D (у відсотках):\nавтори\tфольк", file=file)
        #     print(rel_coef_var_a, rel_coef_var_f, file=file, end='\n\n', sep='\t')
        #
        #     print(f"Відносна похибка:\nавтори\tфольк", file=file)
        #     print(rel_err_a, rel_err_f, file=file, end='\n\n', sep='\t')
        #
        #     if data_a in ["NOUN", "VERB", "CONJ"]:
        #         samples = (data_a, data_f)
        #         unif = check_uniformity(samples)
        #         fr_gr = freedom_greade((len(subs_a)), len(samples))
        #         print(f"Перевірка на статистичну однорідність - х^2:\t", unif, file=file)
        #         print(f"Кількість ступенів свободи:\t", fr_gr, file=file, end='\n\n')
        #
        #     if data_a in ["ADJ", "ADV", "PREP"]:
        #         st_a = standard_error(st_dev_a, len(subs_a), s=True)
        #         st_f = standard_error(st_dev_f, len(subs_f), s=True)
        #         st_cr = students_criterion((mean_a, mean_f), (st_a, st_f))
        #         fr_gr_stud = freedom_greade((sum(subs_a), sum(subs_f)), len(samples), students_criterion_=True)
        #         print(f"Критерій Стьюдента:\t", st_cr, file=file)
        #         print(f"Кількість ступенів свободи:\t", fr_gr_stud, file=file, end='')

        if polygons:
            mpl.rcParams['figure.max_open_warning'] = 0
            frequency_polygon(subs_a, data_a[1]+" authors", show=False, x_max=50, x_ticks_freq=5)
            frequency_polygon_by_intervals(subs_a, data_a[1]+" authors", show=False, x_max=50, x_ticks_freq=5)
            frequency_polygon(subs_f, data_f[1]+" folk", show=False, x_max=50, x_ticks_freq=5)
            frequency_polygon_by_intervals(subs_f, data_f[1] + " folk", show=False, x_max=50, x_ticks_freq=5)


if __name__ == '__main__':
    db = database.Database("tales.db")

    authors_tales = "authors"
    folk_tales = "folk"
    num_of_sub = 200

    # create_tables(authors_tales, db, num_of_sub=num_of_sub, word_forms=True, lemmas=True, pos=True, pos_filter=True)
    # create_tables(folk_tales, db, num_of_sub=num_of_sub, word_forms=True, lemmas=True, pos=True, pos_filter=True)

    # print(authors_tales)
    # authors = db.read_from_table(f"lemmas_authors", where="lemma in ('бути', 'ти', 'дрібний', 'великий')", order_by="abs_freq", num=30, desc=False)
    # print(authors)
    # print("len(authors)", len(authors))
    #
    # print(sum([word[3] for word in authors]))
    # print()
    # print(folk_tales)
    # folk = db.read_from_table(f"lemmas_folk", where="lemma in ('бути', 'ти', 'дрібний', 'великий')", order_by="abs_freq", num=30, desc=False)
    # print(folk)
    # print("len(folk)", len(folk))
    # print(sum([word[3] for word in folk]))

    # do_reading(authors_tales, db, pos_filter=True)
    # print()
    # do_reading(folk_tales, db, pos_filter=True)

    do_calculations(db, table="lemmas", where="lemma = 'бути' AND pos in ('VERB', 'AUX')", order_by="", polygons=True)
    do_calculations(db, table="lemmas", where="lemma = 'ти' AND pos = 'PRON'", order_by="", polygons=True)
    do_calculations(db, table="lemmas", where="lemma = 'дрібний' AND pos in ('DET', 'ADJ')", order_by="", polygons=True)
    do_calculations(db, table="lemmas", where="lemma = 'великий' AND pos in ('DET', 'ADJ')", order_by="", polygons=True)

    db.conn.close()
