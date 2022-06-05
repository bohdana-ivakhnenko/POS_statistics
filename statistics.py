import collections
from collections import defaultdict
import matplotlib.pyplot as plt
from math import log10, sqrt
import re


def checked_title(title: str) -> str:
    """
    Видаляє з назви знаки, які не можуть бути у назві файлу, а також заміняє пробіли на нижні риски
    :param title: назва
    :return: відредагована назва
    """
    return re.sub(r"[|/\\:*?\"<>]", "", title).replace(" ", "_")


def statistical_round(num: float, rounding: int = 2) -> float:
    """
    Окруклює з точністю до необхідних знаків після коми або нулів.
    :param num: число, яке потрібно округлити
    :param rounding: скільки знаків післякоми чи нулів потрібно залишити, дефолтне значення - 2
    :return: округлений дріб
    """
    if rounding == 0:
        round(num+0.00000001)

    num_str = str(num)
    index = num_str.index('.')

    zeros = 0
    if num_str[index+1] == '0':
        zeros = num_str[index+1:].count('0')

    if num_str[index+rounding+zeros+1:index+rounding+zeros+2] == '5':
        num_str = num_str[:index+rounding+zeros+1] + '6' + num_str[index+rounding+zeros+2:]

    return round(float(num_str), rounding+zeros)


def group(frequencies: tuple) -> dict:
    """
    Організовує частоти у *варіаційний* (статистичний) ряд.
    :param frequencies: частоти досліджуваної одиниці у підвибірках
    :return: варіаційний ряд по типу {частота: штуки}
    """
    grouped_freqs = defaultdict(int)
    for freq in frequencies:
        grouped_freqs[freq] += 1
    return dict(sorted(grouped_freqs.items()))


def group_by_intervals(frequencies: tuple) -> dict:
    """
    Організовує частоти у *інтервальний* ряд.
    Кількість інтервалів визначається автоматично.
    :param frequencies: частоти досліджуваної одиниці у підвибірках
    :return: інтервальний ряд по типу {(початок інтервалу - нестрогий, кінець інтервалу - стогий): штуки}
    """
    n = len(frequencies)
    num_of_intervals = 1 + int(3.322 * log10(n))
    h = (max(frequencies) - min(frequencies)) / (num_of_intervals - 1)
    start = min(frequencies) - (h / 2)

    intervals = defaultdict(int)
    for i in range(num_of_intervals):
        end = statistical_round(start + h, 2)
        numbers = [freq for freq in frequencies if start <= freq < end]
        intervals[(start, end)] = len(numbers)
        start = end

    return dict(intervals)


def frequency_polygon_by_intervals(frequencies: tuple, xlabel: str, x_max: int = 400, y_max: int = 70,
                                   x_ticks_freq: int = 20, y_ticks_freq: int = 5,
                                   show: bool = True, path="results\\pos\\freq_his\\") -> None:
    """
    Графік інтервального полігону частот та гістограми.
    :param frequencies: частоти досліджуваної одиниці у підвибірках
    :param xlabel: назва досліджуваної одиниці
    :param x_max: ширина графіка
    :param y_max: висота графіка
    :param show: якщо True, то графік з'явиться на екрані
    :param x_ticks_freq: інтервал рисок на вісі Ох
    :param y_ticks_freq: інтервал рисок на вісі Оy
    :param path: шлях до теки, куди потрібно зберегти графік; якщо вказано "", то файл зберігатися не буде
    :return: None
    """
    plt.figure(figsize=(12, 7))

    n = len(frequencies)
    num_of_intervals = 1 + int(3.322 * log10(n))

    a, bins, c = plt.hist(frequencies, bins=num_of_intervals, histtype='step', linewidth=2.0, color="yellow")
    l = list(bins)
    l.insert(0, 0)
    l.insert(len(bins) + 1, bins[len(bins) - 1])
    mid = []

    for i in range(len(l) - 1):
        el = (l[i] + l[i + 1]) / 2
        mid.append(el)

    x = list(a)
    x.insert(0, 0)
    x.insert(len(a) + 1, 0)
    plt.margins(0.2)

    indent_left = x_max / 25
    indent_right = x_max / 20
    indent_upper = y_max / 15

    plt.xlim([0 - indent_left, x_max + indent_right])
    plt.ylim([0, y_max + indent_upper])
    plt.plot(mid, x, 'royalblue', linewidth=2.0)

    y_labels = [num for num in range(0, y_max + 1, y_ticks_freq)]
    plt.yticks(range(0, y_max + 1, y_ticks_freq), y_labels, fontdict={"size": 11})
    x_labels = [num for num in range(0, x_max + 1, x_ticks_freq)]
    plt.xticks(range(0, x_max + 1, x_ticks_freq), x_labels, rotation=45, fontdict={"size": 11})

    plt.xlabel(f'Інтервали частот {xlabel}', fontdict={"size": 15})
    plt.ylabel('Кількість підвибірок', fontdict={"size": 15})
    plt.title(f"Інтервальні полігон частот і гістограма для {xlabel}", fontdict={"size": 18})
    plt.xlabel(xlabel)

    if path:
        plt.savefig(f'{path}{checked_title(xlabel)}.png', dpi=100)

    if show:
        plt.show()


def frequency_polygon(frequencies: tuple, xlabel: str, x_max=400, y_max=70, show=True, x_ticks_freq=20,
                      y_ticks_freq=5, path="results\\pos\\freq_pol\\"):
    """
    Графік полігону частот.
    :param frequencies: частоти досліджуваної одиниці у підвибірках
    :param xlabel: назва досліджуваної одиниці
    :param x_max: ширина графіка
    :param y_max: висота графіка
    :param show: якщо True, то графік з'явиться на екрані
    :param x_ticks_freq: інтервал рисок на вісі Ох
    :param y_ticks_freq: інтервал рисок на вісі Оy
    :param path: шлях до теки, куди потрібно зберегти графік; має завершуватися на \\;
                 якщо вказано "", то файл зберігатися не буде
    :return: None
    """
    plt.figure(figsize=(12, 7))

    grouped_data = group(frequencies)
    freqs = grouped_data.keys()
    nums = grouped_data.values()
    plt.plot(freqs, nums, linewidth=2.0, color='royalblue')

    indent_left = x_max / 25
    indent_right = x_max / 20
    indent_upper = y_max / 15

    plt.xlim([0 - indent_left, x_max + indent_right])
    plt.ylim([0, y_max + indent_upper])

    y_labels = [num for num in range(0, y_max + 1, y_ticks_freq)]
    plt.yticks(range(0, y_max + 1, y_ticks_freq), y_labels, fontdict={"size": 11})
    x_labels = [num for num in range(0, x_max + 1, x_ticks_freq)]
    plt.xticks(range(0, x_max + 1, x_ticks_freq), x_labels, rotation=45, fontdict={"size": 11})

    plt.xlabel(f'Частоти {xlabel}', fontdict={"size": 15})
    plt.ylabel('Кількість підвибірок', fontdict={"size": 15})
    plt.title(f"Полігон частот на варіаційному ряді {xlabel}", fontdict={"size": 18})

    if path:
        plt.savefig(f'{path}{checked_title(xlabel)}.png', dpi=100)

    if show:
        plt.show()


def arithmetic_mean(grouped_data: dict, intervals=False) -> float:
    """
    Середня арифметична частота з варіаційного (статистичного) ряду. x- (ікс із дашком)
    :param grouped_data: варіаційний чи інтервальний ряд
    :param intervals: чи вказано інтервальний ряд
    :return: середнє арифметичне з частот
    """
    sum_ = 0
    for key, value in grouped_data.items():

        if intervals:
            key = (key[0] + key[1]) / 2

        sum_ += key * value
    return statistical_round(sum_ / sum(grouped_data.values()), 2)


def standard_deviation(grouped_data, arithmetic_mean_: float, interval=False) -> float:
    """
    Середнє квадратичне відхилення. СИГМА
    :param grouped_data: варіаційний ряд частот
    :param arithmetic_mean_: середнє арифметичне
    :param interval: чи варіаційний ряд є інтервальним
    :return: десятковий дріб значення середнього квадратичного відхилення.
    """
    numerator = []
    for x, num in grouped_data.items():
        if interval:
            x = statistical_round((x[0] + x[1]) / 2, 2)

        x_x = statistical_round(x - arithmetic_mean_, 2)
        squared = statistical_round(x_x ** 2, 4)
        numerator.append(squared * num)

    result = sqrt(sum(numerator) / sum(grouped_data.values()))
    return statistical_round(result, 2)


def standard_error(st_dev: float, num_of_freq: int, s: bool) -> float:
    """
    Міра коливання середньої частоти. СИГМА_Х_середнє
    АБО
    Стандартна похибка відхилення середньої (залежить від параметра s).
    :param st_dev: standard deviation | середнє квадратичне відхилення
    :param num_of_freq: number of frequencies | кількість частот
    :param s: якщо True, то функція поверне *стандартну похибку відхилення середньої частоти*
    (важливо, коли вибірок менше 50)
    :return: десятковий дріб *міри коливання середньої частоти* або *стандартної похибки відхилення середньої частоти*
    (залежить від параметра s)
    """
    if s:
        return st_dev / sqrt(num_of_freq - 1)
    return statistical_round(st_dev / sqrt(num_of_freq), 2)


def create_stripe(mean_: float, st_err_dev: float, mtpl: int) -> tuple:
    """
    Обраховує смугу коливання для заданого довірчого інтервалу (похибки).
    При обрахунку із *середнім квадратичним відхиленням* отримуємо коливання середньої частоти у вибірці.
    При обрахунку із *мірою коливання середньої частоти* отримуємо прогноз коливання середньої частоти
    в генеральній сукупності.
    :param mean_: середнє арифметичне
    :param st_err_dev: середнє квадратичне відхилення чи міра коливання середньої частоти
    :param mtpl: 1, 2 або 3, залежно від потрібного коефіцієнта для середнього квадратичного відхилення
    :return: інтервал для смуги коливання
    """
    start = statistical_round(mean_ - (mtpl * st_err_dev))
    end = statistical_round(mean_ + (mtpl * st_err_dev))
    return start, end


def visualise_freq_fluct(stripes_level: dict, all_nums: tuple, title: str, show: bool, path: str, param_type: str,
                         order_of_sub: tuple = ("authors", "folklore"),
                         confidences_full: tuple = (68.3, 95.5, 99.7)) -> None:
    """
    Створює графік для порівняння смуг коливання з двох різних вибірок.
    :param confidences_full: список можливих довірчих інтервалів
    :param stripes_level: інтервали обрахованих смуг коливання
    :param all_nums: всі межі інтервалів з обох вибірок (щоб підписати риски)
    :param show: якщо True, то графік з'явиться на екрані
    :param title: назва досліджуваної одиниці
    :param param_type: st_err для міри коливання середньої частоти і st_dev для середнього квадратичного відхилення
    :param path: шлях до теки, куди потрібно зберегти графік; має завершуватися на \\;
                 якщо вказано "", то файл зберігатися не буде
    :param order_of_sub: порядок вказаних даних, назви вибірок
    :return: None
    """
    plt.figure(figsize=(15, 7))

    mult = 30
    levels_y = list(range(70, 105, 15))
    plt.ylim([60, 110])
    if param_type == "st_dev":
        plt.yticks(levels_y, [f"{conf}%,  {index}σ " for index, conf in enumerate(confidences_full, 1)],
                   fontdict={"size": 11.5})
    elif param_type == "st_err":
        plt.yticks(levels_y, [f"{conf}%,  {index}σ_х̅ " for index, conf in enumerate(confidences_full, 1)],
                   fontdict={"size": 11.5})

    plt.xlim([min(all_nums) * mult - 10, max(all_nums) * mult + 10])
    plt.xticks([x * mult for x in all_nums], all_nums, rotation=45, fontdict={"size": 8.3})

    line_a = plt.Line2D(xdata=(0, 0), ydata=(0, 0), label=order_of_sub[0])
    line_f = plt.Line2D(xdata=(0, 0), ydata=(0, 0), label=order_of_sub[1])
    for stripes, level in zip(stripes_level.values(), levels_y):
        if len(stripes) == 2:
            y_value = level + 3
            line_a, = plt.plot([d * mult for d in stripes[0]], (y_value, y_value), color='forestgreen', linewidth=1.7,
                               label=order_of_sub[0])
            [plt.vlines(x=d * mult, ymin=0, ymax=y_value, colors='forestgreen', linestyles=':', linewidth=1.3, alpha=0.7)
             for d in stripes[0]]

            y_value = level - 3
            line_f, = plt.plot([d * mult for d in stripes[1]], (y_value, y_value), color='steelblue', linewidth=1.7,
                               label=order_of_sub[1])
            [plt.vlines(x=d * mult, ymin=0, ymax=y_value, colors='steelblue', linestyles=':', linewidth=1.3, alpha=0.7)
             for d in stripes[1]]
        else:
            line_a, = plt.plot([d * mult for d in stripes[0]], (level, level), color='forestgreen', linewidth=1.7,
                               label=order_of_sub[0])
            [plt.vlines(x=d * mult, ymin=0, ymax=level, colors='forestgreen', linestyles=':', linewidth=1.3, alpha=0.7)
             for d in stripes[0]]

    # plt.vlines(x=0, ymin=0, ymax=110, colors="black", linestyles='-', linewidth=1, alpha=0.6)

    plt.legend(handles=[line_a, line_f])
    plt.xlabel('Смуги коливання', fontdict={"size": 15})

    if param_type == "st_dev":
        plt.title(f'Cмуги коливання середньої частоти для {title} у вибірці', fontdict={"size": 18})
    elif param_type == "st_err":
        plt.title(f'Cмуги коливання середньої частоти для {title} у генеральній сукупності', fontdict={"size": 18})

    if path:
        plt.savefig(f'{path}{checked_title(title)}.png', dpi=100)

    if show:
        plt.show()


def frequency_fluctuations(arithmetic_means: tuple, st_errs_devs: tuple, param_type: str, visualise: bool,
                           title: str = "", path: str = "freq_str_path\\", order_of_sub: tuple = ("authors", "folklore"),
                           confidences: tuple = (68.3, 95.5, 99.7), show: bool = False) -> dict:
    """
    Cмуги коливання частот для заданих довірчих інтервалів, візуалізації їх у графіку.
    При обрахунку із *середнім квадратичним відхиленням* отримуємо коливання середньої частоти у вибірці.
    При обрахунку із *мірою коливання середньої частоти* отримуємо прогноз коливання середньої частоти
    в генеральній сукупності.
    :param arithmetic_means: значення арифметичних середніх для обох вибірок
    :param st_errs_devs: значення середнього квадратичного відхилення або міри коливання середньої частоти
                         для обох вибірок
    :param param_type: st_err для міри коливання середньої частоти і st_dev для середнього квадратичного відхилення
    :param order_of_sub: назви вибірок у порядку, в якому вказані середнє арифметичне та середнє квадратичне відхилення
    :param visualise: якщо True, то буде автоматично створено графік, який можна буде вивести на екран та/або зберегти
    :param path: шлях до теки, куди потрібно зберегти графік; має завершуватися на \\;
                 якщо вказано "", то файл зберігатися не буде
    :param title: назва досліджуваної одиниці
    :param confidences: кортеж бажаних довірчих інтервалів
    :param show: якщо True, то графік з'явиться на екрані
    :return: інтервали коливання частот для обох вибірок (з назвами, вказаними у order_of_sub)
    """
    confidences_full = (68.3, 95.5, 99.7)
    stripes_type = collections.defaultdict(dict)
    stripes_level = collections.defaultdict(list)
    all_nums = []

    for mtpl, confidence in enumerate(confidences_full, 1):
        for index_, mean_ in enumerate(arithmetic_means):
            if confidences[mtpl - 1] == float(confidence):
                stripe = create_stripe(mean_, st_errs_devs[index_], mtpl)
                stripes_type[order_of_sub[index_]][confidence] = stripe
                stripes_level[confidence].append(stripe)
                all_nums.extend(stripe)

    if visualise:
        visualise_freq_fluct(stripes_level, tuple(all_nums), title, show, path, param_type, order_of_sub,
                             confidences_full)

    return stripes_type


def coefficient_of_variation(st_dev: float, arithmetic_mean_: float) -> float:
    """
    Коефіцієнт варіації V.
    :param st_dev: середнє квадратичне відхилення
    :param arithmetic_mean_: середнє арифметичне
    :return: значення коефіцієнта варіації від 0 до 1
    """
    return statistical_round(st_dev / arithmetic_mean_)


def v_max(num_of_subs) -> float:
    return sqrt(num_of_subs - 1)


def relative_coefficient_of_variation(st_dev: float, arithmetic_mean_: float, num_of_subs: int,
                                      absolute_freq: bool) -> float:
    """
    Коефіцієнт стабільности D.
    :param st_dev: середнє квадратичне відхилення
    :param arithmetic_mean_: середнє арифметичне
    :param num_of_subs: кількість підвирірок
    :param absolute_freq: # насправді ні на що не впливає, але у підручнику було два варіанти обрахунків #
    :return: значення коефіцієнта стабільности від 0 до 1
    """
    if absolute_freq:
        d = 1 - (st_dev / (arithmetic_mean_ * sqrt(num_of_subs - 1)))
    else:
        v = st_dev / arithmetic_mean_
        d = 1 - (v / v_max(num_of_subs))
    return statistical_round(d)


def relative_error(st_err_mean: tuple = (), st_dev_mean_subs_num: tuple = (), var_coef_subs_num: tuple = ()) -> float:
    """
    Відносна похибка дослідження. Обрахунок трьома різними наборами даних - заповніть один із параметрів функції
    (якщо заповнити більше, то результат буде за найостаннішим параметром).
    Порядок вказування даних у кортежі важливий!
    :param st_err_mean: міра коливання середньої частоти: float; середнє арифметичне: float
    :param st_dev_mean_subs_num: середнє квадратичне відхилення: float; середнє арифметичне: float;
                                 кількість підвибірок: int
    :param var_coef_subs_num: коефіцієнт варіації: float; кількість підвибірок: int
    :return: значення відносної похибки
    """
    k = 1.96
    e = 0

    if len(st_err_mean) == 2:
        e = (k * st_err_mean[0]) / st_err_mean[1]
    elif len(st_dev_mean_subs_num) == 3:
        e = (k * st_dev_mean_subs_num[0]) / (st_dev_mean_subs_num[1] * sqrt(st_dev_mean_subs_num[2]))
    elif len(var_coef_subs_num) == 2:
        e = (k * var_coef_subs_num[0]) / sqrt(var_coef_subs_num[1])
    else:
        print("No combination of data fits!")

    return statistical_round(e)


def relative_subtraction(num1, num2) -> float:
    """
    Відносна різниця.
    :param num1: перше число - від нього віднімають і на нього ділять
    :param num2: друге число - його віднімають
    :return: значення відносної різниці
    """
    return statistical_round(abs(num1 - num2) / num1)


def check_uniformity(samples_subs_freqs: tuple) -> float:
    """
    Перевірка на статистичну однорідність, критерій однорідности хі-2
    :param samples_subs_freqs: кортеж кортежів підвибірок вирірок, які потрібно порівняти
    :return: значення критерію однорідности
    """
    abs_sample_freqs = [sum(sample) for sample in samples_subs_freqs]
    total_sum = sum(abs_sample_freqs)

    fractions = []
    for subsample in samples_subs_freqs:
        for index_sub, abs_freq in enumerate(subsample):
            number_squared = abs_freq ** 2
            fraction = number_squared / (sum(subsample) * sum([subs[index_sub] for subs in samples_subs_freqs]))
            fractions.append(fraction)

    x_2 = total_sum * (sum(fractions) - 1)
    return statistical_round(x_2)


def freedom_greade(subsamples: tuple, num_of_samples: int = 0, students_t_test_=False) -> int:
    """
    Підрахунок кількости ступенів свободи.
    :param subsamples: кількість підвибірок
    :param num_of_samples: кількість вибірок
    :param students_t_test_: значення критерію Стьюдента
    :return: кількість ступенів свободи
    """
    if students_t_test_:
        return len(subsamples[0]) + len(subsamples[1]) - 2
    return (len(subsamples[0]) - 1) * (num_of_samples - 1)


def students_t_test(samples_mean_freq: tuple, s_: tuple) -> float:
    """
    Критерій Стьюдента.
    :param samples_mean_freq:
    :param s_:
    :return: значення критерію Стьюдента
    """
    numerator = abs(samples_mean_freq[0] - samples_mean_freq[1])
    denominator = sqrt(s_[0] ** 2 + s_[1] ** 2)
    return statistical_round(numerator / denominator)


def get_sample_size(coef_of_var: float, rel_err: float = 0.045) -> int:
    """
    Точний обрахунок обсягу вибірки для досягнення заданої відносної похибки дослідження.
    :param coef_of_var: коефіцієнт варіації для певної одиниці
    :param rel_err: відносна похибка дослідження (бажана): 0.317 (точність 68.3%), 0.045 (95.5%) чи 0.003 (99.7%)
    :return: кількість підвибірок по 1000 слововживань, необхідні для дослідження одиниці із бажаним рівнем похибки
    """
    k = 1.96
    numerator = (k ** 2) * (coef_of_var ** 2)
    denominator = rel_err ** 2
    return int(statistical_round(numerator / denominator, 0))


def analise_grouped_data(data, whole):
    print("num of freq\t", sum(data.values()))

    number = sum([key * value for key, value in data.items()])
    print("percent of whole", (number / whole) * 100)
    print("out of 100\t", 100 - ((number / whole) * 100))
