"""
Utility functions for lifting capacity calculations.
"""

from app.db.models import CraneDbModel
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
            # interpolate_1d raises value error only if x1 == x2
            except ValueError:
                return None

    return None


def can_crane_lift_payload_at_radius(
    crane: CraneDbModel, radius: float, payload: float
) -> bool:
    """
    Check if a crane can lift the given payload at the specified radius.

    This function checks all lc_tables and all boom lengths to find the
    maximum lifting capacity at the given radius. If any configuration
    can lift the payload, the crane is considered capable.

    Args:
        crane: Crane database model
        radius: Radius in meters
        payload: Required payload in tons

    Returns:
        True if the crane can lift the payload at the radius, False otherwise
    """
    # Check all lc_tables
    for lc_table_data in crane.lc_tables.values():
        table = lc_table_data.get("table", {})

        # Check all boom lengths
        for radius_capacity_map in table.values():
            lifting_capacity = get_lifting_capacity_at_radius(
                radius_capacity_map, radius
            )
            if lifting_capacity is not None and lifting_capacity >= payload:
                return True

    return False
