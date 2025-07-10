from sqlalchemy.orm import Query

from app.db.models import CraneDbModel
from app.schemas.cranes import ChassisType


def filter_cranes_by_name(queryset: Query, name: str) -> Query:
    """
    Filter a queryset of cranes by model name using substring matching.

    Args:
        query (Query): SQLAlchemy query object containing cranes
        name (str): Substring to search for in crane models (case-insensitive)

    Returns:
        Query: SQLAlchemy query object containing filtered cranes
    """
    return queryset.filter(CraneDbModel.model.ilike(f"%{name}%"))


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
