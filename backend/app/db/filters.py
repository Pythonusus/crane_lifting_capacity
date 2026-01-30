from sqlalchemy.orm import Query

from app.db.models import CraneDbModel
from app.schemas.cranes import ChassisType
from app.settings import FRIENDLY_COUNTRIES
from utils.lifting_capacity import get_lifting_capacity_at_radius


def filter_cranes_by_model(queryset: Query, model: str) -> Query:
    """
    Filter a queryset of cranes by model using substring matching.

    Args:
        query (Query): SQLAlchemy query object containing cranes
        model (str): Substring to search for in crane models (case-insensitive)

    Returns:
        Query: SQLAlchemy query object containing filtered cranes
    """
    # !!!IMPORTANT!!!
    # Get all cranes and filter in Python for better Russian character support
    # Heavy and slow approach, but the only way to make russian named models
    # to be searched case-insensitive.
    # Refactor if filtering becomes to slow with db grow.
    all_cranes = queryset.all()
    filtered_cranes = [
        crane for crane in all_cranes if model.lower() in crane.model.lower()
    ]

    # Return a new query with the filtered IDs
    crane_ids = [crane.id for crane in filtered_cranes]
    return queryset.filter(CraneDbModel.id.in_(crane_ids))


def filter_cranes_by_chassis_type(
    queryset: Query, chassis_type: ChassisType
) -> Query:
    """
    Filter a queryset of cranes by their chassis type.

    Args:
        query (Query): SQLAlchemy query object containing cranes
        chassis_type (ChassisType): Chassis type to filter by

    Returns:
        Query: SQLAlchemy query object containing filtered cranes
    """
    return queryset.filter(CraneDbModel.chassis_type == chassis_type)


def filter_cranes_by_manufacturer(queryset: Query, manufacturer: str) -> Query:
    """
    Filter a queryset of cranes by their manufacturer.

    Args:
        query (Query): SQLAlchemy query object containing cranes
        chassis_type (ChassisType): Chassis type to filter by

    Returns:
        Query: SQLAlchemy query object containing filtered cranes
    """
    return queryset.filter(CraneDbModel.manufacturer == manufacturer)


def filter_cranes_by_max_lifting_capacity(
    queryset: Query,
    min_max_lifting_capacity: float | None,
    max_max_lifting_capacity: float | None,
) -> Query:
    """
    Filter a queryset of cranes by their max lifting capacity.
    """
    if min_max_lifting_capacity is not None:
        queryset = queryset.filter(
            CraneDbModel.max_lifting_capacity >= min_max_lifting_capacity
        )
    if max_max_lifting_capacity is not None:
        queryset = queryset.filter(
            CraneDbModel.max_lifting_capacity <= max_max_lifting_capacity
        )
    return queryset


def filter_cranes_by_country(queryset: Query, country: str) -> Query:
    """
    Filter a queryset of cranes by their country.
    """
    if country == "РФ и дружественные страны":
        return queryset.filter(CraneDbModel.country.in_(FRIENDLY_COUNTRIES))

    return queryset.filter(CraneDbModel.country == country)


def _can_radius_capacity_map_lift_payload(
    radius_capacity_map: dict, radius: float, payload: float
) -> bool:
    """
    Check if a radius-capacity mapping can provide enough lifting capacity
    at the specified radius to lift the payload.

    Args:
        radius_capacity_map: Dictionary mapping radius (string keys) to
            lifting capacity
        radius: Radius in meters to check
        payload: Required payload in tons

    Returns:
        True if the mapping indicates the payload can be lifted, False otherwise
    """
    lifting_capacity = get_lifting_capacity_at_radius(
        radius_capacity_map, radius
    )
    return lifting_capacity is not None and lifting_capacity >= payload


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
    for table_name, lc_table_data in crane.lc_tables.items():
        table = lc_table_data.get("table", {})

        # Check all boom lengths
        for boom_length, radius_capacity_map in table.items():
            if _can_radius_capacity_map_lift_payload(
                radius_capacity_map, radius, payload
            ):
                return True

    return False


def filter_cranes_by_deep_filtering(
    queryset: Query, radius: float, payload: float
) -> Query:
    """
    Deep filtering: For each chassis_type and manufacturer combination,
    find the cheapest crane that can lift the payload at the given radius.

    This filter should be applied FIRST, before other filters.

    Args:
        queryset: SQLAlchemy query object containing cranes
        radius: Radius in meters
        payload: Required payload in tons

    Returns:
        Query: SQLAlchemy query object containing filtered cranes
    """
    # Get all cranes (we need to load lc_tables to check capacity)
    all_cranes = queryset.all()

    # Group by chassis_type and manufacturer
    groups = {}
    for crane in all_cranes:
        key = (crane.chassis_type, crane.manufacturer)
        if key not in groups:
            groups[key] = []
        groups[key].append(crane)

    # For each group, find cranes that can lift the payload
    # and select the cheapest
    selected_crane_ids = []
    for (chassis_type, manufacturer), cranes in groups.items():
        # Filter cranes that can lift the payload at the radius
        capable_cranes = [
            crane
            for crane in cranes
            if can_crane_lift_payload_at_radius(crane, radius, payload)
        ]

        if not capable_cranes:
            # No crane in this group can lift the payload
            continue

        # Find the cheapest crane (by base_price)
        cheapest_crane = min(
            capable_cranes, key=lambda c: c.base_price
        )
        selected_crane_ids.append(cheapest_crane.id)

    # Return query filtered by selected crane IDs
    if not selected_crane_ids:
        # No cranes match the criteria, return empty query
        return queryset.filter(CraneDbModel.id.in_([]))

    return queryset.filter(CraneDbModel.id.in_(selected_crane_ids))
