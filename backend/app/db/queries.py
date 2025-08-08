from typing import List

from sqlalchemy.orm import Session, noload

from app.db.filters import (
    filter_cranes_by_chassis_type,
    filter_cranes_by_manufacturer,
    filter_cranes_by_max_lifting_capacity,
    filter_cranes_by_model,
)
from app.db.models import CraneBinaryAttachmentDbModel, CraneDbModel
from app.schemas.cranes import CraneFilterRequest


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
    parts = crane_name.split('_', 1)

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


def get_cranes_db_models_by_filters(
    db: Session, filters: CraneFilterRequest
) -> List[CraneDbModel]:
    """
    Get a list of cranes by filters.
    """
    # Simplified query to reduce memory usage for list views
    queryset = db.query(CraneDbModel).options(
        noload(CraneDbModel.attachments),  # Exclude attachments
    )

    if filters.model:
        queryset = filter_cranes_by_model(queryset, filters.model)
    if filters.manufacturer:
        queryset = filter_cranes_by_manufacturer(queryset, filters.manufacturer)
    if filters.chassis_type:
        queryset = filter_cranes_by_chassis_type(queryset, filters.chassis_type)
    if filters.min_max_lc or filters.max_max_lc:
        queryset = filter_cranes_by_max_lifting_capacity(
            queryset, filters.min_max_lc, filters.max_max_lc
        )
    return queryset.all()


def get_manufacturers_from_db(db: Session) -> List[str]:
    """
    Get all available manufacturers.
    """
    manufacturers = db.query(CraneDbModel.manufacturer).distinct().all()
    return [manufacturer[0] for manufacturer in manufacturers]


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
    parts = crane_name.split('_', 1)
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
