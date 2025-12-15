"""
Schemas for crane-related API endpoints
"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    computed_field,
    field_validator,
)

from app.settings import SUPPORTED_IMAGE_CONTENT_TYPES


class ChassisType(str, Enum):
    """Class containing all available chassis types"""

    # TODO: Uncomment when we have data for these chassis types
    TRUCK_MOUNTED = "Автомобильный"
    MOBILE = "Спецшасси автомобильного типа"
    CRAWLER = "Гусеничный"
    RAILWAY = "Железнодорожный"
    # TOWER = "Башенный"


class ChassisTypesResponse(BaseModel):
    """Response model for chassis types"""

    chassisTypes: list[str] = [chassy_type.value for chassy_type in ChassisType]


class SortOption(BaseModel):
    """Single sorting option"""

    key: str
    text: str
    value: str


class SortOptionsResponse(BaseModel):
    """Response model for sorting options"""

    sortOptions: List[SortOption] = [
        SortOption(
            key="displayNameAsc",
            text="Название крана (А-Я)",
            value="displayNameAsc",
        ),
        SortOption(
            key="displayNameDesc",
            text="Название крана (Я-А)",
            value="displayNameDesc",
        ),
        SortOption(
            key="maxCapacityAsc", text="Макс г/п ↑", value="maxCapacityAsc"
        ),
        SortOption(
            key="maxCapacityDesc", text="Макс г/п ↓", value="maxCapacityDesc"
        ),
        SortOption(
            key="pricePerHourAsc",
            text="Стоимость маш.-ч ↑",
            value="pricePerHourAsc",
        ),
        SortOption(
            key="pricePerHourDesc",
            text="Стоимость маш.-ч ↓",
            value="pricePerHourDesc",
        ),
    ]


class CraneMetadataAttachment(BaseModel):
    """Attachment metadata for API responses (without binary data)"""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    filename: str
    content_type: str

    @computed_field
    def is_inline(self) -> bool:
        return self.content_type in SUPPORTED_IMAGE_CONTENT_TYPES


class CraneBinaryAttachment(CraneMetadataAttachment):
    """Full attachment model with binary data (for internal backend usage)"""

    data: bytes


class LcTable(BaseModel):
    """Lifting capacity table"""

    radiuses: List[str]
    table: Dict[str, Dict[str, float]]

    @field_validator("table")
    def validate_table(cls, table):
        for radius_capacity in table.values():
            for radius, capacity in radius_capacity.items():
                if float(radius) <= 0:
                    raise ValueError("Radius must be positive")
                if capacity <= 0:
                    raise ValueError("Capacity must be positive")
        return table

    @computed_field
    def boom_lengths(self) -> list[str]:
        return list(self.table.keys())


class CraneListItem(BaseModel):
    """Simplified crane model for list views (better performance)"""

    model_config = ConfigDict(from_attributes=True)

    # Basic information
    id: Optional[int] = None
    model: str
    manufacturer: str
    country: str
    chassis_type: ChassisType
    max_lifting_capacity: float = Field(gt=0)

    # Economic section
    resource_code: str
    base_price: float = Field(gt=0)
    labor_cost: float = Field(gt=0)

    @computed_field
    def name(self) -> str:
        return f"{self.manufacturer}_{self.model}"

    @computed_field
    def price_per_hour(self) -> float:
        return round(self.base_price + self.labor_cost, 2)


class Crane(BaseModel):
    """Full crane model for detail views"""

    model_config = ConfigDict(from_attributes=True)

    # Basic information
    id: Optional[int] = None
    model: str
    manufacturer: str
    country: str
    chassis_type: ChassisType
    max_lifting_capacity: float = Field(gt=0)
    description: Optional[str] = None
    manufacturer_url: Optional[HttpUrl] = None
    crane_url: Optional[HttpUrl] = None
    lc_tables: Dict[str, LcTable]  # Key is lc_table name

    # Economic section
    pricebook: str
    resource_code: str
    base_price: float = Field(gt=0)
    labor_cost: float = Field(gt=0)

    # Attachments section
    dwg_url: Optional[HttpUrl] = None
    attachments: Optional[List[CraneMetadataAttachment]] = None

    @computed_field
    def name(self) -> str:
        return f"{self.manufacturer}_{self.model}"

    @computed_field
    def price_per_hour(self) -> float:
        return round(self.base_price + self.labor_cost, 2)

    @computed_field
    def lc_tables_names(self) -> list[str]:
        return list(self.lc_tables.keys())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class CraneFilterRequest(BaseModel):
    """Filter criteria for cranes"""

    model: Optional[str] = None
    manufacturer: Optional[str] = None
    chassis_type: Optional[ChassisType] = None
    country: Optional[str] = None
    min_max_lc: Optional[float] = Field(None, gt=0)
    max_max_lc: Optional[float] = Field(None, gt=0)
    sortBy: Optional[str] = None
    # Load-more pagination parameters
    offset: Optional[int] = Field(
        0, ge=0, description="Number of items to skip"
    )
    limit: Optional[int] = Field(
        15, ge=1, le=100, description="Number of items to return"
    )


class CraneListResponse(BaseModel):
    """Response model for load-more crane list"""

    cranes: List[CraneListItem]
    cranes_count: int = Field(
        description="Total number of cranes matching filters"
    )
    has_more: bool = Field(description="Whether there are more items available")
    returned_count: int = Field(
        description="Number of items returned in this response"
    )
