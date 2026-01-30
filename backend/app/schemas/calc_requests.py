from typing import Optional

from pydantic import BaseModel, Field


class LcCalcRequest(BaseModel):
    """
    Calculate crane lifting capacity for given crane, boom length and radius.
    """
    crane_name: str
    table_name: Optional[str] = "Основная стрела"
    boom_len: str
    radius: float = Field(gt=0)  # in meters


class PayloadCalcRequest(LcCalcRequest):
    """
    Calculate max available payload for given
    equipment weight and safety factor.
    """
    equipment_weight: float = Field(ge=0)  # in tonns
    safety_factor: float = Field(gt=0)


class SafetyFactorCalcRequest(LcCalcRequest):
    """
    Calculate safety factor for given equipment weight and payload.
    """
    equipment_weight: float = Field(ge=0)  # in tonns
    payload: float = Field(gt=0)  # in tonns
