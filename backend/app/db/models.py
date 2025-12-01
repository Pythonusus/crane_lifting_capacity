from sqlalchemy import (
    JSON,
    Column,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import deferred, relationship

from app.db.session import Base


class CraneDbModel(Base):
    """
    Represents a crane in the database.
    Deferred columns are not loaded into memory by default.
    They will be lazy loaded when needed.
    """

    __tablename__ = "cranes"

    # Basic information
    id = Column(Integer, primary_key=True)
    model = deferred(Column(String, nullable=False))
    manufacturer = deferred(Column(String, nullable=False))
    country = deferred(Column(String, nullable=False))
    chassis_type = deferred(Column(String, nullable=False))
    max_lifting_capacity = deferred(Column(Float, nullable=False))
    description = deferred(Column(Text, nullable=True))
    manufacturer_url = deferred(Column(String, nullable=True))
    crane_url = deferred(Column(String, nullable=True))
    # LC tables: stored as JSON with structure:
    # {"table_name": {"boom_lengths": [...], "radiuses": [...], "table": {...}}}
    lc_tables = deferred(Column(JSON, nullable=False))

    # Economic section
    pricebook = deferred(Column(String, nullable=False))
    resource_code = deferred(Column(String, nullable=False))
    base_price = deferred(Column(Float, nullable=False))
    labor_cost = deferred(Column(Float, nullable=False))

    # Attachments section
    dwg_url = deferred(Column(String, nullable=True))
    # Lazy loaded by default
    attachments = relationship(
        "CraneBinaryAttachmentDbModel", back_populates="crane"
    )

    # Manufacturer + model combination is unique
    __table_args__ = (
        UniqueConstraint("manufacturer", "model", name="uq_manufacturer_model"),
    )

    @property
    def name(self) -> str:
        return f"{self.manufacturer}_{self.model}"

    @property
    def price_per_hour(self) -> float:
        return round(self.base_price + self.labor_cost, 2)

    @property
    def lc_tables_names(self) -> list[str]:
        return list(self.lc_tables.keys())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class CraneBinaryAttachmentDbModel(Base):
    """Represents a single binary attachment in the database."""

    __tablename__ = "crane_binary_attachments"

    id = Column(Integer, primary_key=True)
    crane_id = Column(Integer, ForeignKey("cranes.id"), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    crane = relationship("CraneDbModel", back_populates="attachments")
