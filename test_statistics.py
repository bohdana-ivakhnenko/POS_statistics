import pytest
import statistics

_test_cases_group = [
    ((2, 3, 4, 5, 2, 3, 1, 4, 5, 4, 0),
     ((0, 1), (1, 1), (2, 2), (3, 2), (4, 3), (5, 2)))
]


@pytest.mark.parametrize("test_case", _test_cases_group)
def test_create_table(test_case):
    result = statistics.group(test_case[0])
    assert set(test_case[1]) == set(result)


if __name__ == '__main__':
    test_create_table()
