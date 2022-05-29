import pytest
import statistics


_test_cases_round = [
    (0.072, 0.072),
    (1.0192, 1.019),
    (1.0199, 1.02),
    (1.0239, 1.024),
    (1.98, 1.98),
    (1.998, 2.0),
    (1.991, 1.99),
    (1.335, 1.34),
    (0.00335, 0.0034),
    (1.555, 1.56)
]


@pytest.mark.parametrize("test_case", _test_cases_round)
def test_round(test_case):
    result = statistics.statistical_round(test_case[0])
    assert result == test_case[1]


_test_cases_group = [
    ((2, 3, 4, 5, 2, 3, 1, 4, 5, 4, 0),
     {0: 1, 1: 1, 2: 2, 3: 2, 4: 3, 5: 2}),
    ((0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4,
      5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9),
     {0: 2, 1: 2, 2: 4, 3: 6, 4: 6, 5: 3, 6: 3, 7: 6, 8: 4, 9: 4})
]


@pytest.mark.parametrize("test_case", _test_cases_group)
def test_group(test_case):
    result = statistics.group(test_case[0])
    assert result == test_case[1]


_test_cases_group_int = [
    ((0.79, 0.90, 0.99, 0.95, 0.91, 0.80, 0.99, 0.88, 0.86, 0.95,
      0.98, 0.90, 0.89, 0.78, 0.88, 0.87, 1.00, 0.84, 0.95, 0.78,
      0.94, 0.97, 0.99, 1.00, 0.82, 1.00, 0.87, 0.95, 0.92, 0.92,
      0.96, 0.84, 0.96, 0.82, 0.91, 0.76, 0.77, 0.88, 0.83, 0.90,
      0.97, 0.99, 0.82, 0.78, 1.00, 0.98, 0.90, 0.87, 1.00, 0.99,
      0.86, 0.86, 0.76, 0.95, 0.89, 0.99, 0.79, 0.99, 1.00, 0.77,
      0.86, 0.95, 1.00, 1.00, 0.82, 0.99, 0.90, 0.82, 0.98, 0.94,
      0.98, 0.92, 0.84, 1.00, 0.88, 0.84, 1.00, 0.86, 0.99, 0.94,
      0.94, 0.94, 0.89, 0.98, 0.79, 0.99, 0.94, 0.97, 0.94, 0.94,
      0.87, 0.97, 1.00, 0.99, 0.99, 0.93, 0.91, 0.83, 0.79, 0.99),
     {(0.74, 0.78): 4, (0.78, 0.82): 8, (0.82, 0.86): 11, (0.86, 0.9): 16,
      (0.9, 0.94): 12, (0.94, 0.98): 20, (0.98, 1.02): 29})
]


@pytest.mark.parametrize("test_case", _test_cases_group_int)
def test_group_int(test_case):
    result = statistics.group_by_intervals(test_case[0])
    assert result == test_case[1]


_test_cases_mean = [
    ({0: 59, 1: 85, 2: 71, 3: 51, 4: 16, 5: 13, 6: 5, 7: 4, 8: 1},
     1.89)
]


@pytest.mark.parametrize("test_case", _test_cases_mean)
def test_mean(test_case):
    result = statistics.arithmetic_mean(test_case[0])
    assert result == test_case[1]


_test_cases_mean_int = [
    (
        {(6.0, 8.4): 16, (8.4, 10.8): 13, (10.8, 13.2): 12, (13.2, 15.6): 6, (15.6, 18.0): 3},
        10.42
    ),
    (
        {(4.8, 7.2): 11, (7.2, 9.6): 11, (9.6, 12.0): 14, (12.0, 14.4): 7, (14.4, 16.8): 6, (16.8, 19.2): 1},
        10.27
    )
]


@pytest.mark.parametrize("test_case", _test_cases_mean_int)
def test_mean_int(test_case):
    result = statistics.arithmetic_mean(test_case[0], intervals=True)
    assert result == test_case[1]


_test_cases_st_dev = [
    ({0: 59, 1: 85, 2: 71, 3: 51, 4: 16, 5: 13, 6: 5, 7: 4, 8: 1},
     1.58)
]


@pytest.mark.parametrize("test_case", _test_cases_st_dev)
def test_st_dev(test_case):
    stable_mean_ = statistics.arithmetic_mean(test_case[0])
    result = statistics.standard_deviation(test_case[0], stable_mean_=stable_mean_)
    assert result == test_case[1]


_test_cases_st_dev_int = [
    ({(6.0, 8.4): 16, (8.4, 10.8): 13, (10.8, 13.2): 12, (13.2, 15.6): 6, (15.6, 18.0): 3},
     2.90)
]


@pytest.mark.parametrize("test_case", _test_cases_st_dev_int)
def test_st_dev_int(test_case):
    stable_mean_ = statistics.arithmetic_mean(test_case[0], intervals=True)
    result = statistics.standard_deviation(test_case[0], stable_mean_=stable_mean_, interval=True)
    assert result == test_case[1]


_test_cases_st_error = [
    ({"st_dev": 1.25, "num_of_freq": 305},
     0.072)
]


@pytest.mark.parametrize("test_case", _test_cases_st_error)
def test_st_error(test_case):
    result = statistics.standard_error(test_case[0]["st_dev"], test_case[0]["num_of_freq"])
    assert result == test_case[1]


_test_cases_freq_fluct = [
    ({"mean": 1.89, "st_dev": 1.25},
     {68.3: (0.64, 3.14), 95.5: (-0.61, 4.39), 99.7: (-1.86, 5.64)})
]


@pytest.mark.parametrize("test_case", _test_cases_freq_fluct)
def test_freq_fluct(test_case):
    result = statistics.frequency_fluctuations(test_case[0]["mean"], test_case[0]["st_dev"], visualise=False)
    assert result == test_case[1]


if __name__ == '__main__':
    test_round()
    test_group()
    test_group_int()
    test_mean()
    test_mean_int()
    test_st_dev()
    test_st_dev_int()
    test_st_error()
