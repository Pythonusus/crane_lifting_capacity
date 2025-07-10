from typing import List

from sqlalchemy.orm import Session

from app.db.filters import (
    filter_cranes_by_chassis_type,
    filter_cranes_by_manufacturer,
    filter_cranes_by_max_lifting_capacity,
    filter_cranes_by_name,
)
from app.db.models import CraneDbModel
from app.schemas.cranes import CraneFilterRequest


def get_crane_by_id(db: Session, crane_id: int) -> CraneDbModel | None:
    """
    Retrieve a crane from the database by its ID.

    Args:
        db (Session): SQLAlchemy database session
        crane_id (int): ID of the crane to retrieve

    Returns:
        Crane | None: The crane object if found, None otherwise
    """
    return db.query(CraneDbModel).filter(CraneDbModel.id == crane_id).first()


def get_cranes_by_filters(
    db: Session, filters: CraneFilterRequest
) -> List[CraneDbModel]:
    """
    Get a list of cranes by filters.
    Note: sortBy is ignored as sorting is handled on the frontend.
    """
    queryset = db.query(CraneDbModel)

    if filters.name:
        queryset = filter_cranes_by_name(queryset, filters.name)
    if filters.manufacturer:
        queryset = filter_cranes_by_manufacturer(queryset, filters.manufacturer)
    if filters.chassis_type:
        queryset = filter_cranes_by_chassis_type(queryset, filters.chassis_type)
    if filters.min_max_lc or filters.max_max_lc:
        queryset = filter_cranes_by_max_lifting_capacity(
            queryset, filters.min_max_lc, filters.max_max_lc
        )
    # Note: filters.sortBy is ignored as sorting is handled on the frontend
    return queryset.all()


def get_manufacturers_from_db(db: Session) -> List[str]:
    """
    Get all available manufacturers.
    """
    manufacturers = db.query(CraneDbModel.manufacturer).distinct().all()
    return [manufacturer[0] for manufacturer in manufacturers]
