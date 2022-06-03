import collections
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import text
from math import log10, sqrt
import numpy as np


def statistical_round(num: float, rounding: int = 2) -> float:
    """
    Функція що дозволяє окруклювати з точністю до необхідних знаків після коми або нулів.
    :param num: число, яке потрібно округлити
    :param rounding: скільки знаків потрібно залишити, дефолтне значення - 2
    :return: округлений дріб
    """
    num_str = str(num)
    index = num_str.index('.')

    zeros = 0
    if num_str[index+1] == '0':
        zeros = num_str[index+1:].count('0')

    if num_str[index+rounding+zeros+1:index+rounding+zeros+2] == '5':
        num_str = num_str[:index+rounding+zeros+1] + '6' + num_str[index+rounding+zeros+2:]

    return round(float(num_str), rounding+zeros)


# варіаційний ряд
def group(frequencies: tuple) -> dict:
    grouped_freqs = defaultdict(int)
    for freq in frequencies:
        grouped_freqs[freq] += 1
    return dict(sorted(grouped_freqs.items()))


# інтервальний ряд
def group_by_intervals(frequencies: tuple) -> dict:
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


# полігон частот
def frequency_polygon_by_intervals(data: tuple, xlabel: str, x_max=400, y_max=70, show=True, x_ticks_freq=20,
                                   path="results\\pos\\freq_his\\") -> None:
    plt.figure(figsize=(12, 7))

    n = len(data)
    num_of_intervals = 1 + int(3.322 * log10(n))

    a, bins, c = plt.hist(data, bins=num_of_intervals, histtype='step')
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
    plt.plot(mid, x, 'yellow')

    y_labels = [num for num in range(0, y_max + 1, 5)]
    plt.yticks(range(0, y_max + 1, 5), y_labels)
    x_labels = [num for num in range(0, x_max + 1, x_ticks_freq)]
    plt.xticks(range(0, x_max + 1, x_ticks_freq), x_labels, rotation=45)

    plt.xlabel(f'Інтервали частот {xlabel}')
    plt.ylabel('Кількість підвибірок')
    plt.title(f"Інтервальні полігон частот і гістограма для {xlabel}")
    plt.xlabel(xlabel)

    plt.savefig(f'{path}{xlabel}.png', dpi=100)

    if show:
        plt.show()


def frequency_polygon(data: tuple, xlabel: str, x_max=400, y_max=70, show=True, x_ticks_freq=20,
                      path="results\\pos\\freq_pol\\"):
    plt.figure(figsize=(12, 7))

    grouped_data = group(data)
    freqs = grouped_data.keys()
    nums = grouped_data.values()
    plt.plot(freqs, nums)

    indent_left = x_max / 25
    indent_right = x_max / 20
    indent_upper = y_max / 15

    plt.xlim([0 - indent_left, x_max + indent_right])
    plt.ylim([0, y_max + indent_upper])

    y_labels = [num for num in range(0, y_max + 1, 5)]
    plt.yticks(range(0, y_max + 1, 5), y_labels)
    x_labels = [num for num in range(0, x_max + 1, x_ticks_freq)]
    plt.xticks(range(0, x_max + 1, x_ticks_freq), x_labels, rotation=45)

    plt.xlabel(f'Частоти {xlabel}')
    plt.ylabel('Кількість підвибірок')
    plt.title(f"Полігон частот на варіаційному ряді {xlabel}")

    plt.savefig(f'{path}{xlabel}.png', dpi=100)

    if show:
        plt.show()


# середня частота x-
def arithmetic_mean(grouped_data: dict, intervals=False) -> float:
    sum_ = 0
    for key, value in grouped_data.items():

        if intervals:
            key = (key[0] + key[1]) / 2

        sum_ += key * value
    return statistical_round(sum_ / sum(grouped_data.values()), 2)


def standard_deviation(grouped_data, arithmetic_mean_: float, interval=False) -> float:
    """
    Cереднє квадратичне відхилення. СИГМА
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
    Стандартна похибка відхилення середньої
    :param st_dev: standard deviation | середнє квадратичне відхилення
    :param num_of_freq: number of frequencies | кількість частот
    :param s: якщо True, то функція поверне *стандартну похибку відхилення середньої частоти*
    (важливо, коли вибірок менше 50)
    :return: десятковий дріб *міри коливання середньої частоти* або *стандартну похибку відхилення середньої частоти*
    (залежить від параметра s)
    """
    if s:
        return st_dev / sqrt(num_of_freq - 1)
    return statistical_round(st_dev / sqrt(num_of_freq), 2)


# смуги коливання частот
def frequency_fluctuations(arithmetic_means: tuple, st_devs: tuple, visualise: bool, path: str,
                           order_of_sub: tuple = ("authors", "folklore"), confidences: tuple = (68.3, 95.5, 99.7),
                           show: bool = False) -> tuple:
    stripes = collections.defaultdict(dict)
    confidences_full = (68.3, 95.5, 99.7)

    for mltpl, confidence in enumerate(confidences_full, 1):
        for index, mean_ in enumerate(arithmetic_means):
            if confidences[mltpl-1] == float(confidence):
                start = statistical_round(mean_ - (mltpl * st_devs[index]))
                end = statistical_round(mean_ + (mltpl * st_devs[index]))
            else:
                start = 0
                end = 0
            stripes[order_of_sub[index]][confidence] = (start, end)

    if visualise:
        plt.figure(figsize=(15, 7))

        data = collections.defaultdict(list)
        x_ticks = [0]

        # чи можна інтегрувати в попередній цикл?
        for index, level in enumerate(confidences_full, 1):
            for key, dict_ in stripes[index].items():
                data[key].append(dict_)
                x_ticks.extend(dict_)

        mult = 30
        levels_y = list(range(70, 105, 15))
        plt.ylim([60, 110])
        plt.yticks(levels_y, [f"{conf}%,  {index}σ " for index, conf in enumerate(confidences_full, 1)],
                   fontdict={"size": 11})
        plt.xlim([min(x_ticks)*mult-10, max(x_ticks)*mult+10])
        plt.xticks([x*mult for x in x_ticks], x_ticks, rotation=45, fontdict={"size": 8.3})

        for data_, level in zip(data.values(), levels_y):
            y_value = level + 3
            line_a, = plt.plot([d*mult for d in data_[0]], (y_value, y_value), color='green', linewidth=1.7,
                               label='authors')
            [plt.vlines(x=d*mult, ymin=0, ymax=y_value, colors='green', linestyles=':', linewidth=1.3, alpha=0.7)
             for d in data_[0]]
            print("here")
            y_value = level - 3
            line_f, = plt.plot([d*mult for d in data_[1]], (y_value, y_value), color='blue', linewidth=1.7,
                               label='folklore')
            [plt.vlines(x=d*mult, ymin=0, ymax=y_value, colors='blue', linestyles=':', linewidth=1.3, alpha=0.7)
             for d in data_[1]]
        plt.vlines(x=0, ymin=0, ymax=110, colors="black", linestyles='-', linewidth=1, alpha=0.6)
        plt.legend(handles=[line_a, line_f])

        plt.xlabel('Смуги коливання', fontdict={"size": 14})
        plt.title('Cмуги коливання частот, залежно від довірчих інтервалів', fontdict={"size": 16})

        # plt.savefig(f'{path}{xlabel}.png', dpi=100)

        if show:
            plt.show()

    return tuple(stripes.values())


# коефіцієнт варіації у відсотках - V
def coefficient_of_variation(st_dev: float, arithmetic_mean_: float) -> float:
    return statistical_round(st_dev / arithmetic_mean_)


# коефіцієнт стабільности  (від 0 до 1) - D
def relative_coefficient_of_variation(st_dev: float, arithmetic_mean_: float, number_of_freq, absolute_freq: bool):
    if absolute_freq:
        d = 1 - (st_dev / (arithmetic_mean_ * sqrt(number_of_freq - 1)))
    else:
        v = st_dev / arithmetic_mean_
        v_max = sqrt(number_of_freq - 1)
        d = 1 - (v / v_max)
    return statistical_round(d)


# відносна похибка
def relative_error(st_err_mean=(), st_dev_mean_freq_num=(), var_coef_freq_num=()) -> float:
    k = 1.96
    e = 0

    if len(st_err_mean) == 2:
        e = (k * st_err_mean[0]) / st_err_mean[1]
    elif len(st_dev_mean_freq_num) == 3:
        e = (k * st_dev_mean_freq_num[0]) / (st_dev_mean_freq_num[1] * sqrt(st_dev_mean_freq_num[2]))
    elif len(var_coef_freq_num) == 2:
        e = (k * var_coef_freq_num[0]) / sqrt(var_coef_freq_num[1])
    else:
        print("No combination of data fits!")

    return statistical_round(e)


def relative_subtraction(num1, num2) -> float:
    return statistical_round(abs(num1 - num2) / num1)


# перевірка на статистичну однорідність, хі-2
def check_uniformity(samples_subs_freqs: tuple) -> int:
    abs_sample_freqs = [sum(sample) for sample in samples_subs_freqs]
    total_sum = sum(abs_sample_freqs)
    abs_subsample_freqs = [0] * len(samples_subs_freqs[0])

    for index_sample, sample in enumerate(samples_subs_freqs):
        for index_sub, abs_freq in enumerate(sample[index_sample]):
            abs_subsample_freqs[index_sub] += abs_freq

    fractions = []
    for index_sample, sample in enumerate(samples_subs_freqs):
        for index_sub, abs_freq in enumerate(sample[index_sample]):
            number_squared = abs_freq ** 2
            fraction = number_squared / ((sum(sample)) * abs_subsample_freqs[index_sub])
            fractions.append(fraction)

    x_2 = total_sum * (sum(fractions) - 1)
    return x_2


# кількість ступенів свободи
def freedom_greade(num_of_subsamples: tuple, num_of_samples: int, students_criterion_=False):
    if students_criterion_:
        return sum(num_of_subsamples) - len(num_of_subsamples)
    return (num_of_subsamples[0] - 1) * (num_of_samples - 1)


# критерій Стьюдента
def students_criterion(samples_mean_freq: tuple, s_: tuple) -> float:
    numerator = abs(samples_mean_freq[0] - samples_mean_freq[1])
    denominator = sqrt(s_[0] ** 2 + s_[1] ** 2)
    return statistical_round(numerator / denominator)


# Необхідний обсяг вибірки для досягнення заданої відносної похибки дослідження
def get_sample_size(coef_of_var: float, rel_err: float = 0.045) -> int:
    k = 1.96
    numerator = (k ** 2) * (coef_of_var ** 2)
    denominator = rel_err ** 2
    return int(statistical_round(numerator / denominator, 0))


# x = (78, 72, 69, 81, 63, 67, 65, 75, 9, 100, 100, 400, 400, 350, 350, 400, 74, 1, 83, 71, 79, 80, 69)
# frequency_polygon_by_intervals(x, 'NOUN frequency')
# frequency_polygon(x, 'NOUN frequency polygon')
# print(frequency_fluctuations((1.89,), (1.25,), visualise=True))
print(frequency_fluctuations((1.89, 2.55), (1.25, 1.0), visualise=True, path="", show=True))
