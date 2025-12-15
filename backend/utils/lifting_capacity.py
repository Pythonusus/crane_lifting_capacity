"""
Utility functions for lifting capacity calculations.
"""

from utils.math import get_nearest_greater, get_nearest_lesser, interpolate_1d


def get_lifting_capacity_at_radius(
    radius_capacity_map: dict, radius: float
) -> float | None:
    """
    Calculate lifting capacity at a given radius from a radius-capacity mapping.

    This function handles direct matches and interpolation when needed.
    It can be used for both service calculations and filtering operations.

    Args:
        radius_capacity_map: Dictionary mapping radius (string keys) to
            lifting capacity values
        radius: Radius in meters

    Returns:
        Lifting capacity if calculable, None otherwise
    """
    if not radius_capacity_map:
        return None

    # Create mapping from float values to original string keys.
    # This is necessary because keys are strings, but we need to use them
    # as floats for finding nearest values. And then we need to convert them
    # back to strings to use as keys in the map.
    float_to_str_map = {float(k): k for k in radius_capacity_map.keys()}
    float_keys = list(float_to_str_map.keys())

    # Check for direct match first
    str_radius = float_to_str_map.get(radius)
    if str_radius is not None:
        return radius_capacity_map.get(str_radius)

    # Need interpolation
    nearest_lesser = get_nearest_lesser(radius, float_keys)
    nearest_greater = get_nearest_greater(radius, float_keys)

    if nearest_lesser is not None and nearest_greater is not None:
        # Both bounds available - interpolate
        lc_less = radius_capacity_map.get(float_to_str_map[nearest_lesser])
        lc_greater = radius_capacity_map.get(float_to_str_map[nearest_greater])

        if lc_less is not None and lc_greater is not None:
            try:
                return interpolate_1d(
                    float(radius),
                    nearest_lesser,
                    lc_less,
                    nearest_greater,
                    lc_greater,
                )
            except ValueError:
                return None

    # Fallback to nearest value if only one bound available
    if nearest_lesser is not None:
        return radius_capacity_map.get(float_to_str_map[nearest_lesser])

    if nearest_greater is not None:
        return radius_capacity_map.get(float_to_str_map[nearest_greater])

    return None
