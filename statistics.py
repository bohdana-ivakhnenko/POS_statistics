from collections import defaultdict
import matplotlib.pyplot as plt
from math import log10


# варіаційний ряд
def group(frequencies) -> tuple:
    grouped_freqs = defaultdict(int)
    for freq in frequencies:
        grouped_freqs[freq] += 1
    return tuple(grouped_freqs.items())


# інтервальний ряд
def grouped_by_intervals(frequencies: list) -> dict:
    n = len(frequencies)
    num_of_intervals = 1 + int(log10(n))
    h = (max(frequencies) - min(frequencies)) / (num_of_intervals - 1)
    start = min(frequencies) - (h / 2)

    intervals = defaultdict(int)
    for i in range(num_of_intervals):
        numbers = [freq for freq in frequencies if start < freq < (start + h)]
        intervals[(start, start + h)] = len(numbers)

    return intervals


# полігон частот
# має бути 2 варіанти: для чисел та інтервалів
def frequency_polygon(data: tuple, xlabel: str) -> None:
    n = len(data)
    num_of_intervals = 1 + int(log10(n))
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


# коефіцієнт варіації у відсотках - V
def coefficient_of_variation():
    pass


# коефіцієнт стабільности  (від 0 до 1) - D
def relative_coefficient_of_variation():
    pass


# середнє квадратичне відхилення
def standard_deviation():
    pass


# міра коливання середньої частоти
def standard_error():
    pass


# смуги коливання частот
def visualise_frequency_fluctuations():
    pass


# відносна похибка
def relative_error():
    pass


# x = (78, 72, 69, 81, 63, 67, 65, 75, 9, 74, 1, 83, 71, 79, 80, 69)
# frequency_polygon(x, 'NOUN frequency')
