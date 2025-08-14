import pytest

from utils.math import (
    get_nearest_greater,
    get_nearest_lesser,
    interpolate_1d,
)


def test_get_nearest_lesser(cranes_test_data):
    num_list = [5, 15, 16, 17, 18, 19, 20]
    assert get_nearest_lesser(16, num_list) == 15
    assert get_nearest_lesser(15.5, num_list) == 15
    assert get_nearest_lesser(1, num_list) is None
    assert get_nearest_lesser(5, num_list) is None


def test_get_nearest_greater(cranes_test_data):
    num_list = [10, 12, 14, 16, 18, 20, 50]
    assert get_nearest_greater(10.32, num_list) == 12
    assert get_nearest_greater(16, num_list) == 18
    assert get_nearest_greater(1000, num_list) is None
    assert get_nearest_greater(50, num_list) is None


def test_interpolate_1d():
    assert interpolate_1d(12.5, 12, 56.4, 13, 55.5) == 55.95
    assert interpolate_1d(12.5, 12, 56.4, 13, 56.4) == 56.4
    assert pytest.raises(ValueError, interpolate_1d, 12.5, 12, 56.4, 12, 58.0)
