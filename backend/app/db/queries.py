from typing import List

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, noload

from app.db.filters import (
    filter_cranes_by_chassis_type,
    filter_cranes_by_country,
    filter_cranes_by_manufacturer,
    filter_cranes_by_max_lifting_capacity,
    filter_cranes_by_model,
)
from app.db.models import CraneBinaryAttachmentDbModel, CraneDbModel
from app.schemas.cranes import CraneFilterRequest
from app.settings import FRIENDLY_COUNTRIES, PAGINATION_SIZE


def get_crane_db_model_by_name(
    db: Session, crane_name: str
) -> CraneDbModel | None:
    """
    Retrieve a crane from the database by its name (manufacturer + model).

    Args:
        db (Session): SQLAlchemy database session
        crane_name (str): Name of the crane (format: "Manufacturer Model")

    Returns:
        Crane | None: The crane object if found, None otherwise
    """
    # Split the name into manufacturer and model
    parts = crane_name.split("_", 1)

    if len(parts) != 2:
        return None

    manufacturer, model = parts
    return (
        db.query(CraneDbModel)
        .filter(
            CraneDbModel.manufacturer == manufacturer,
            CraneDbModel.model == model,
        )
        .first()
    )


def _apply_sorting_to_cranes_query(query, sort_by: str | None = None):
    """
    Apply sorting to cranes query based on sort_by parameter.

    Args:
        query: SQLAlchemy Query object
        sort_by: Sort criteria identifier

    Returns:
        SQLAlchemy Query object with sorting applied
    """
    # Define sorting options mapping
    sorting_options = {
        "displayNameAsc": [
            asc(CraneDbModel.manufacturer),
            asc(CraneDbModel.model),
        ],
        "displayNameDesc": [
            desc(CraneDbModel.manufacturer),
            desc(CraneDbModel.model),
        ],
        "maxCapacityAsc": [asc(CraneDbModel.max_lifting_capacity)],
        "maxCapacityDesc": [desc(CraneDbModel.max_lifting_capacity)],
        "pricePerHourAsc": [
            asc(CraneDbModel.base_price + CraneDbModel.labor_cost)
        ],
        "pricePerHourDesc": [
            desc(CraneDbModel.base_price + CraneDbModel.labor_cost)
        ],
    }

    # Default sorting: by display name (manufacturer + model) ascending
    default_sorting = [asc(CraneDbModel.manufacturer), asc(CraneDbModel.model)]

    # Get sorting criteria or use default
    sort_criteria = sorting_options.get(sort_by, default_sorting)

    return query.order_by(*sort_criteria)


def _build_filtered_cranes_query(
    db: Session, filters: CraneFilterRequest | None = None
):
    """
    Helper function to build the base filtered query for cranes.

    Args:
        db: Database session
        filters: Filter criteria

    Returns:
        SQLAlchemy Query object with filters applied
    """
    base_query = db.query(CraneDbModel)

    if filters is None:
        return base_query

    # Apply filters
    if filters.model:
        base_query = filter_cranes_by_model(base_query, filters.model)
    if filters.manufacturer:
        base_query = filter_cranes_by_manufacturer(
            base_query, filters.manufacturer
        )
    if filters.chassis_type:
        base_query = filter_cranes_by_chassis_type(
            base_query, filters.chassis_type
        )
    if filters.country:
        base_query = filter_cranes_by_country(base_query, filters.country)
    if filters.min_max_lc or filters.max_max_lc:
        base_query = filter_cranes_by_max_lifting_capacity(
            base_query, filters.min_max_lc, filters.max_max_lc
        )

    return base_query


def get_filtered_cranes_count(
    db: Session, filters: CraneFilterRequest | None = None
) -> int:
    """
    Get the total count of cranes matching the given filters.

    Args:
        db: Database session
        filters: Filter criteria

    Returns:
        Total number of cranes matching the filters
    """
    base_query = _build_filtered_cranes_query(db, filters)
    return base_query.count()


def get_cranes_db_models_by_filters(
    db: Session, filters: CraneFilterRequest | None = None
) -> List[CraneDbModel]:
    """
    Get a list of cranes matching the given filters
    with offset-based pagination and sorting.

    Args:
        db: Database session
        filters: Filter criteria with offset/limit parameters and sorting

    Returns:
        List of CraneDbModel objects
    """
    # Build query with optimizations for list views
    base_query = _build_filtered_cranes_query(db, filters).options(
        noload(CraneDbModel.attachments),  # Exclude attachments for performance
    )

    # Apply sorting
    sort_by = filters.sortBy if filters else None
    sorted_query = _apply_sorting_to_cranes_query(base_query, sort_by)

    # Apply offset-based pagination
    offset = filters.offset or 0 if filters else 0
    limit = filters.limit or PAGINATION_SIZE if filters else PAGINATION_SIZE

    return sorted_query.offset(offset).limit(limit).all()


def get_manufacturers_from_db(db: Session) -> List[str]:
    """
    Get all available manufacturers.
    """
    manufacturers = db.query(CraneDbModel.manufacturer).distinct().all()
    return [manufacturer[0] for manufacturer in manufacturers]


def get_countries_from_db(db: Session) -> List[str]:
    """
    Get all available countries.
    Includes "РФ и дружественные страны" option if any friendly countries exist.
    """
    countries = db.query(CraneDbModel.country).distinct().all()
    country_list = [country[0] for country in countries]

    # Check if any friendly countries exist in the database
    has_friendly_countries = any(
        country in country_list for country in FRIENDLY_COUNTRIES
    )

    # Add "РФ и дружественные страны" option if applicable
    if has_friendly_countries:
        country_list.insert(0, "РФ и дружественные страны")

    return country_list


def get_crane_id_by_name(db: Session, crane_name: str) -> int | None:
    """
    Get crane ID by crane name.

    Args:
        db: Database session
        crane_name: Name of the crane (format: "Manufacturer_Model")

    Returns:
        Crane ID if found, None otherwise
    """
    # Split the crane name to get manufacturer and model
    parts = crane_name.split("_", 1)
    if len(parts) != 2:
        return None

    manufacturer, model = parts

    # Get only the crane ID
    crane = (
        db.query(CraneDbModel.id)
        .filter(
            CraneDbModel.manufacturer == manufacturer,
            CraneDbModel.model == model,
        )
        .first()
    )

    return crane.id if crane else None


def get_crane_attachment_db_model_by_id(
    db: Session, attachment_id: int
) -> CraneBinaryAttachmentDbModel | None:
    """
    Get a crane attachment by its ID.
    """
    return (
        db.query(CraneBinaryAttachmentDbModel)
        .filter(CraneBinaryAttachmentDbModel.id == attachment_id)
        .first()
    )
