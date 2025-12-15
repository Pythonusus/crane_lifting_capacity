from sqlalchemy.orm import Query

from app.db.models import CraneDbModel
from app.schemas.cranes import ChassisType
from app.settings import FRIENDLY_COUNTRIES


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
