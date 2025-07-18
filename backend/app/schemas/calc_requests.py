from pydantic import BaseModel, Field


class LcCalcRequestBase(BaseModel):
    """
    Calculate crane lifting capacity for given crane, boom length and radius.
    """
    crane_id: int
    boom_len: str
    radius: float = Field(gt=0)  # in meters


class PayloadCalcRequestBase(LcCalcRequestBase):
    """
    Calculate max available payload for given
    equipment weight and safety factor.
    """
    equipment_weight: float = Field(ge=0)  # in tonns
    safety_factor: float = Field(gt=0)


class SafetyFactorCalcRequestBase(LcCalcRequestBase):
    """
    Calculate safety factor for given equipment weight and payload.
    """
    equipment_weight: float = Field(ge=0)  # in tonns
    payload: float = Field(gt=0)  # in tonns


class PayloadCalcRequest(BaseModel):
    base_requests: list[PayloadCalcRequestBase]


class SafetyFactorCalcRequest(BaseModel):
    base_requests: list[SafetyFactorCalcRequestBase]
