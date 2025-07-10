from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ChassisType(str, Enum):
    TRUCK_MOUNTED = "Автомобильный"
    MOBILE = "Спецшасси автомобильного типа"
    CRAWLER = "Гусеничный"
    RAILWAY = "Железнодорожный"
    TOWER = "Башенный"


class ChassisTypesResponse(BaseModel):
    chassisTypes: list[str] = [chassy_type.value for chassy_type in ChassisType]


class CraneBinaryAttachment(BaseModel):
    id: int
    crane_id: int
    filename: str
    content_type: str
    data: bytes

    class Config:
        from_attributes = True


class Crane(BaseModel):
    id: Optional[int] = None
    model: str
    manufacturer: str
    chassis_type: ChassisType
    pricebook: str
    resource_code: str
    base_price: float = Field(gt=0)
    labor_cost: float = Field(gt=0)
    max_lifting_capacity: float = Field(gt=0)
    lc_table: Dict[str, Dict[float, float]]
    attachments: Optional[List[CraneBinaryAttachment]] = None
    blueprint_dwg: Optional[bytes] = None
    lc_table_xls: Optional[bytes] = None
    lc_table_png: Optional[bytes] = None

    @field_validator('lc_table')
    def validate_lc_table(cls, lc_table):
        for _, radius_capacity in lc_table.items():
            for radius, capacity in radius_capacity.items():
                if radius <= 0:
                    raise ValueError("Radius must be positive")
                if capacity <= 0:
                    raise ValueError("Capacity must be positive")
        return lc_table

    @property
    def name(self) -> str:
        return f"{self.manufacturer} {self.model}"

    @property
    def price_per_hour(self) -> float:
        return self.base_price + self.labor_cost

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
    class Config:
        from_attributes = True
