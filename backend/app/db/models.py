from sqlalchemy import (
    JSON,
    Column,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
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

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False, unique=True)
    manufacturer = Column(String, nullable=False)
    chassis_type = Column(String, nullable=False)
    pricebook = Column(String, nullable=False)
    resource_code = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    labor_cost = Column(Float, nullable=False)
    max_lifting_capacity = Column(Float, nullable=False)
    lc_table = deferred(Column(JSON, nullable=False))
    attachments = relationship(
        "CraneBinaryAttachment", back_populates="crane"
    )  # lazy loaded by default

    @property
    def display_name(self) -> str:
        return f"{self.manufacturer} {self.model}"

    @property
    def price_per_hour(self) -> float:
        return self.base_price + self.labor_cost

    def __repr__(self) -> str:
        return self.display_name


class CraneBinaryAttachment(Base):
    """Represents a single binary attachment in the database."""

    __tablename__ = "crane_binary_attachments"

    id = Column(Integer, primary_key=True)
    crane_id = Column(Integer, ForeignKey("cranes.id"), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
    crane = relationship("CraneDbModel", back_populates="attachments")
