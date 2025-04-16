from sqlalchemy.orm import Session

from app.db.models import CraneDbModel
from app.schemas.cranes import ChassisType


def get_all_cranes(db: Session) -> list[CraneDbModel]:
    """
    Retrieve a list of all cranes from the database.
    """
    return db.query(CraneDbModel).all()


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


def get_cranes_by_chassis_type(
    db: Session, chassis_type: ChassisType
) -> list[CraneDbModel]:
    """
    Retrieve a list of cranes from the database by their chassis type.
    """
    return (
        db.query(CraneDbModel)
        .filter(CraneDbModel.chassis_type == chassis_type)
        .all()
    )
