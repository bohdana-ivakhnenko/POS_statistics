from collections import defaultdict
import matplotlib.pyplot as plt
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
    return dict(grouped_freqs)


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


# todo: полігон частот
# має бути 2 варіанти: для чисел та інтервалів
def frequency_polygon(data: tuple, xlabel: str) -> None:
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
    plt.plot(mid, x, 'yellow')
    plt.title(f"Полігон частот для {xlabel}")
    plt.xlabel(xlabel)
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
    :param st_dev: standard deviation | середнє квадратичне відхилення
    :param num_of_freq: number of frequencies | кількість частот
    :param s: якщо True, то функція поверне *стандартну похибку відхилення середньої частоти*
    (важливо, коли вибірок менше 50)
    :return: десятковий дріб *міри коливання середньої частоти* або *стандартну похибку відхилення середньої частоти*
    (залежить від параметра s)
    """
    return statistical_round(st_dev / sqrt(num_of_freq), 2)


# todo: смуги коливання частот
def frequency_fluctuations(arithmetic_mean_: float, st_dev: float, visualise: bool, confidences: tuple = (68.3, 95.5, 99.7)):
    stripes = {}
    confidences_full = (68.3, 95.5, 99.7)

    for mltpl, confidence in enumerate(confidences_full, 1):
        if confidences[mltpl-1] == confidence:
            start = statistical_round(arithmetic_mean_ - (mltpl * st_dev))
            end = statistical_round(arithmetic_mean_ + (mltpl * st_dev))
        else:
            start = 0
            end = 0
        stripes[confidence] = (start, end)

    print(stripes)
    if visualise:
        plt.rcdefaults()
        fig, ax = plt.subplots()

        y_pos = np.arange(len(confidences_full))
        x_value = np.arange(len(stripes.values()))

        ax.barh(y_pos, x_value, align='center')
        ax.set_yticks(y_pos, labels=confidences_full)
        ax.invert_yaxis()  # labels read top-to-bottom

        ax.set_xlabel('Смуги коливання')
        ax.set_title('Cмуги коливання частот, залежно від довірчих інтервалів')
        plt.show()

    return stripes


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


# x = (78, 72, 69, 81, 63, 67, 65, 75, 9, 74, 1, 83, 71, 79, 80, 69)
# frequency_polygon(x, 'NOUN frequency')
# frequency_fluctuations(1.89, 1.25, visualise=True)
