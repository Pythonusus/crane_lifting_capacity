def get_nearest_lesser(
    target: float | int, num_list: list[float | int]
) -> float | int | None:
    """
    Get the nearest lesser value from a list of numbers.
    """
    lesser_nums = [val for val in num_list if val < target]
    if not lesser_nums:
        return None
    return max(lesser_nums)


def get_nearest_greater(
    target: float | int, num_list: list[float | int]
) -> float | int | None:
    """
    Get the nearest greater to target value from a list of numbers.
    """
    greater_nums = [val for val in num_list if val > target]
    if not greater_nums:
        return None
    return min(greater_nums)


def interpolate_1d(
    x: float | int,
    x1: float | int,
    y1: float | int,
    x2: float | int,
    y2: float | int,
) -> float:
    """
    Perform linear interpolation on the given data points.

    Args:
        x (float | int): The x-coordinate of the point to interpolate.
        x1 (float | int): The x-coordinate of the first point.
        y1 (float | int): The y-coordinate of the first point.
        x2 (float | int): The x-coordinate of the second point.
        y2 (float | int): The y-coordinate of the second point.

    Raises:
        ValueError: If the x-coordinates of the points are the same.

    Returns:
        float: The interpolated y-coordinate.
    """
    if x1 == x2:
        raise ValueError("Undefined slope: x1 and x2 cannot be the same")

    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
