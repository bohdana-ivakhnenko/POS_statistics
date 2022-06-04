import processing
import database
import statistics as st
import matplotlib as mpl


def create_a_table(sample_name: str, table_type: str, columns, num_of_sub: int, data, auto_num) -> None:
    """
    Організовує створення таблиці:
    - збирає назву;
    - збирає список атрибутів (стовпчиків);
    - створює таблицю;
    - заносить у неї необхідні значення (рядки).
    :param sample_name: назва вибірки (authors, folk)
    :param table_type: тип таблиці (word_forms, lemmas, pos, pos_filtered)
    :param columns: список назв атрибутів (без підвибірок)
    :param num_of_sub: кількість підвибірок
    :param data: рядки з даними для таблиці
    :param auto_num: якщо True, то нумерацію буде створено автоматично
    :return: None
    """
    table_name = f"{table_type}_{sample_name}"
    columns = columns + tuple([(f"'{num}'", 'INT') for num in range(1, num_of_sub+1)])
    print(db.create_table(table_name, columns, autoincrement=auto_num, drop=True))
    db.insert_into_table(table_name, data, multiple_rows=True)


def create_tables(sample_name: str, db, num_of_sub=0,
                  word_forms=False, lemmas=False, pos=False, pos_filter=False, auto_num=False) -> None:
    """
    Збірна функція, що організовує аналіз даних і створення таблиць для вибірки.
    :param sample_name: назва вибірки (authors, folk)
    :param db: об'єкт бази даних
    :param num_of_sub: кількість підвибірок
    :param word_forms: якщо True, то буде створено таблицю словоформ
    :param lemmas: якщо True, то буде створено таблицю лем
    :param pos: якщо True, то буде створено таблицю частин мови
    :param pos_filter: якщо True, то буде створено таблицю посортованих частин мови
    :param auto_num: якщо True, то в усіх таблицях нумерацію буде створено автоматично
    :return: None
    """
    with open(f"sources\\tales_{sample_name}.txt", "r", encoding="utf-8") as file:
        text = file.read()

    word_forms_data = ()
    if word_forms:
        print("START on WORD FORMS")
        word_forms_subs = processing.into_subsamples(text, num_of_sub)
        print("SUBSAMPLES IN", sample_name, ':\t', num_of_sub)

        word_forms_data = processing.into_word_forms_table(word_forms_subs, auto_num=auto_num)
        columns = (('id', 'INT'), ('word_form', 'TEXT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(sample_name, 'word_forms', columns, num_of_sub, word_forms_data, auto_num)
    elif lemmas:
        word_forms_data = db.read_from_table(f"word_forms_{sample_name}")
        num_of_sub = len(word_forms_data[0]) - 5
    print("Finished on WORD FORMS")

    lemmas_data = ()
    if lemmas:
        print("START on LEMMAS")
        lemmas_data = processing.into_lemmas_table(word_forms_data, auto_num=auto_num)
        columns = (('id', 'INT'), ('lemma', 'TEXT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(sample_name, 'lemmas', columns, num_of_sub, lemmas_data, auto_num)
    elif pos or pos_filter:
        lemmas_data = db.read_from_table(f"lemmas_{sample_name}")
    print("Finished on LEMMAS")

    if pos:
        print("START on POS")
        pos_data = processing.into_pos_table(lemmas_data, auto_num=auto_num)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(sample_name, 'pos', columns, num_of_sub, pos_data, auto_num)

    if pos_filter:
        print("START on filtering POS")
        pos_filter_data = processing.into_pos_table(lemmas_data, auto_num=auto_num, filter_=True)
        columns = (('id', 'INT'), ('pos', 'TEXT'), ('abs_freq', 'INT'))
        create_a_table(sample_name, 'pos_filtered', columns, num_of_sub, pos_filter_data, auto_num)
    print("Finished on POS")


def do_reading(sample_name: str, db, num_of_rows: int = -1,
               word_forms=False, lemmas=False, pos=False, pos_filter=False) -> None:
    """
    Збірна функція для зчитування даних із багатьох таблиць.
    :param sample_name: назва вибірки (authors, folk)
    :param db: об'єкт бази даних
    :param num_of_rows: кількість рядків, які буде виведено на екран; якщо -1, то всі.
    :param word_forms: якщо True, то буде зчитано таблицю словоформ
    :param lemmas: якщо True, то буде зчитано таблицю лем
    :param pos: якщо True, то буде зчитано таблицю частин мови
    :param pos_filter: якщо True, то буде зчитано таблицю посортованих частин мови
    :return: None
    """
    if word_forms:
        data = db.read_from_table(f"word_forms_{sample_name}")
        print("num of word forms: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if lemmas:
        data = db.read_from_table(f"lemmas_{sample_name}", order_by="abs_freq")
        print("num of lemmas: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if pos:
        data = db.read_from_table(f"pos_{sample_name}", order_by="abs_freq")
        print("num of pos: ", len(data))
        [print(line) for line in data[:num_of_rows]]

    if pos_filter:
        data = db.read_from_table(f"pos_filtered_{sample_name}", order_by="abs_freq")
        print("num of pos filtered: ", len(data))
        [print(line) for line in data[:num_of_rows]]


def do_calculations(db, table="pos_filtered", polygons=True, freq_str=True, where="",
                    results_path="results\\pos\\", freq_hist_path="freq_hist\\", freq_pol_path="freq_pol\\",
                    freq_str_path="freq_stripes\\",
                    show=False, x_max=400, x_ticks_freq=20) -> None:
    """
    Збірна функція для виконання всіх необхідних статистичних обрахунків.
    :param db: об'єкт бази даних
    :param table: назва таблиці
    :param polygons: якщо True, то буде створено графіки полігонів частот (і гістограм)
    :param freq_str: якщо True, то буде створено графіки смуг коливання
    :param where: фільтр пошуку - додається до запиту напряму, без перетворень!
    :param results_path: шлях до теки з результатами обрахунків
    :param freq_hist_path: шлях до теки, де будуть файли з інтервальними полігоном частот та гістограмою
    :param freq_pol_path: шлях до теки, де будуть файли із графіками звичайного полігону частот
    :param freq_str_path: шлях до теки, де будуть файли із графіками смуг коливання
    :param show: якщо True, то буде виведено на екран всі створені графіки
    :param x_max: ширина осі Х (до якого числа)
    :param x_ticks_freq: частота малювання рисок на осі Х
    :return: None
    """
    index = 3
    if table.startswith("word_form"):
        index = 5
    elif table.startswith("lemma"):
        index = 4
    elif table.startswith("pos"):
        index = 3

    authors_ = db.read_from_table(f"{table}_authors", where=where, order_by="pos")
    folk_ = db.read_from_table(f"{table}_folk", where=where, order_by="pos")

    for data_a, data_f in zip(authors_, folk_):
        subs_a = data_a[index:]
        subs_f = data_f[index:]

        grouped_a = st.group(subs_a)
        grouped_f = st.group(subs_f)

        grouped_intervals_a = st.group_by_intervals(subs_a)
        grouped_intervals_f = st.group_by_intervals(subs_f)

        mean_a = st.arithmetic_mean(grouped_a)
        mean_f = st.arithmetic_mean(grouped_f)

        st_dev_a = st.standard_deviation(grouped_a, mean_a)
        st_dev_f = st.standard_deviation(grouped_f, mean_f)

        st_err_a = st.standard_error(st_dev_a, len(subs_a), s=False)
        st_err_f = st.standard_error(st_dev_f, len(subs_f), s=False)

        if freq_str:
            stripes = st.frequency_fluctuations((mean_a, mean_f), (st_dev_a, st_dev_f), visualise=True, show=show,
                                                path=results_path+freq_str_path, title=data_a[1])
        else:
            stripes = st.frequency_fluctuations((mean_a, mean_f), (st_dev_a, st_dev_f), visualise=False)

        coef_var_a = st.coefficient_of_variation(st_dev_a, mean_a)
        coef_var_f = st.coefficient_of_variation(st_dev_f, mean_f)

        rel_coef_var_a = st.relative_coefficient_of_variation(st_dev_a, mean_a, len(subs_a), data_a[2])
        rel_coef_var_f = st.relative_coefficient_of_variation(st_dev_f, mean_f, len(subs_f), data_f[2])

        rel_err_a = st.relative_error((st_err_a, mean_a))
        rel_err_f = st.relative_error((st_err_f, mean_f))

        sample_size_a = st.get_sample_size(coef_var_a)
        sample_size_f = st.get_sample_size(coef_var_f)

        with open(f"{results_path}{data_a[1]}.txt", "w", encoding="utf-8") as file:
            print(f"Абсолютна частота автори:\t", data_a[index-1], file=file, end='\n\n')
            print(f"Абсолютна частота фольк:\t", data_f[index-1], file=file, end='\n\n')

            print(f"Варіаційний ряд автори:", file=file)
            print(grouped_a, file=file, end='\n\n')
            print(f"Варіаційний ряд фольк:", file=file)
            print(grouped_f, file=file, end='\n\n')

            print(f"Інтервальний ряд автори:", file=file)
            print(grouped_intervals_a, file=file, end='\n\n')
            print(f"Інтервальний ряд фольк:", file=file)
            print(grouped_intervals_f, file=file, end='\n\n')

            print(f"Середнє арифметичне:\nавтори\tфольк", file=file)
            print(mean_a, mean_f, file=file, end='\n\n', sep='\t')

            print(f"Середнє квадратичне відхилення:\nавтори\tфольк", file=file)
            print(st_dev_a, st_dev_f, file=file, end='\n\n', sep='\t')

            print(f"Міра коливання середньої частоти:\nавтори\tфольк", file=file)
            print(st_err_a, st_err_f, file=file, end='\n\n', sep='\t')

            print(f"Смуги коливання:\nавтори\tфольк", file=file)
            print(stripes["authors"], stripes["folklore"], file=file, end='\n\n', sep='\t')

            print(f"Коефіцієнт варіації - V (у відсотках):\nавтори\tфольк", file=file)
            print(coef_var_a, coef_var_f, file=file, end='\n\n', sep='\t')

            print(f"Коефіцієнт стабільности - D (у відсотках):\nавтори\tфольк", file=file)
            print(rel_coef_var_a, rel_coef_var_f, file=file, end='\n\n', sep='\t')

            print(f"Відносна похибка:\nавтори\tфольк", file=file)
            print(rel_err_a, rel_err_f, file=file, end='\n\n', sep='\t')

            print(f"Кількість підвибірок по 1000 слововживань для відносної похибки у 4,5%:\nавтори\tфольк", file=file)
            print(sample_size_a, sample_size_f, file=file, end='\n\n', sep='\t')

            print(f"Приклад рядка автори:", file=file)
            print(data_a, file=file)
            print(f"Приклад рядка фольк:", file=file)
            print(data_f, file=file)

            if data_a in ["NOUN", "VERB", "CONJ"]:
                samples = (data_a, data_f)
                unif = st.check_uniformity(samples)
                fr_gr = st.freedom_greade((len(subs_a),), len(samples))
                print(f"Перевірка на статистичну однорідність - х^2:\t", unif, file=file)
                print(f"Кількість ступенів свободи:\t", fr_gr, file=file, end='\n\n')

            if data_a in ["ADJ", "ADV", "PREP"]:
                st_a = st.standard_error(st_dev_a, len(subs_a), s=True)
                st_f = st.standard_error(st_dev_f, len(subs_f), s=True)
                st_t_test = st.students_t_test((mean_a, mean_f), (st_a, st_f))
                fr_gr_stud = st.freedom_greade((sum(subs_a), sum(subs_f)), len(samples), students_criterion_=True)
                print(f"Критерій Стьюдента:\t", st_t_test, file=file)
                print(f"Кількість ступенів свободи:\t", fr_gr_stud, file=file, end='')

        if polygons:
            mpl.rcParams['figure.max_open_warning'] = 0
            st.frequency_polygon(subs_a, data_a[1]+" authors", show=show, x_max=x_max, x_ticks_freq=x_ticks_freq,
                                 path=results_path+freq_pol_path)
            st.frequency_polygon(subs_f, data_f[1] + " folk", show=show, x_max=x_max, x_ticks_freq=x_ticks_freq,
                                 path=results_path + freq_pol_path)
            st.frequency_polygon_by_intervals(subs_a, data_a[1]+" authors", show=show, x_max=x_max,
                                              x_ticks_freq=x_ticks_freq, path=results_path+freq_hist_path)
            st.frequency_polygon_by_intervals(subs_f, data_f[1] + " folk", show=show, x_max=x_max,
                                              x_ticks_freq=x_ticks_freq, path=results_path+freq_hist_path)


if __name__ == '__main__':
    db = database.Database("tales.db")

    authors_tales = "authors"
    folk_tales = "folk"
    num_of_sub = 200

    # СТВОРЕННЯ
    # create_tables(authors_tales, db, num_of_sub=num_of_sub, word_forms=True, lemmas=True, pos=True, pos_filter=True)
    # create_tables(folk_tales, db, num_of_sub=num_of_sub, word_forms=True, lemmas=True, pos=True, pos_filter=True)

    # ЧИТАННЯ СПЕЦІАЛЬНЕ
    # print(authors_tales)
    # authors = db.read_from_table(f"lemmas_authors", where="lemma in ('бути', 'ти', 'дрібний', 'великий')",
    #                              order_by="abs_freq", num=30, desc=False)
    # print(authors)
    # print("len(authors)", len(authors))
    #
    # print(sum([word[3] for word in authors]))
    # print()
    # print(folk_tales)
    # folk = db.read_from_table(f"lemmas_folk", where="lemma in ('бути', 'ти', 'дрібний', 'великий')",
    #                           order_by="abs_freq", num=30, desc=False)
    # print(folk)
    # print("len(folk)", len(folk))
    # print(sum([word[3] for word in folk]))

    # ЧИТАННЯ ЗАГАЛЬНЕ
    # do_reading(authors_tales, db, pos_filter=True)
    # print()
    # do_reading(folk_tales, db, pos_filter=True)

    # ОБРАХУНКИ
    do_calculations(db, polygons=True, freq_str=True)
    do_calculations(db, table="lemmas", where="lemma = 'бути' AND pos in ('VERB', 'AUX')",
                    polygons=True, freq_str=True, results_path="results\\high_freq\\", x_max=50, x_ticks_freq=5)

    do_calculations(db, table="lemmas", where="lemma = 'ти' AND pos = 'PRON'",
                    polygons=True, freq_str=True, results_path="results\\high_freq\\", x_max=50, x_ticks_freq=5)

    do_calculations(db, table="lemmas", where="lemma = 'дрібний' AND pos in ('DET', 'ADJ')",
                    polygons=True, freq_str=True, results_path="results\\low_freq\\", x_max=50, x_ticks_freq=5)

    do_calculations(db, table="lemmas", where="lemma = 'великий' AND pos in ('DET', 'ADJ')",
                    polygons=True, freq_str=True, results_path="results\\low_freq\\", x_max=50, x_ticks_freq=5)

    db.conn.close()
