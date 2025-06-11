from pydantic import BaseModel

from app.schemas.calc_requests import (
    LcCalcRequestBase,
    PayloadCalcRequest,
    PayloadCalcRequestBase,
    SafetyFactorCalcRequest,
    SafetyFactorCalcRequestBase,
)


class LcCalcResponseBase(BaseModel):
    request: LcCalcRequestBase
    lifting_capacity: float


class SafetyFactorCalcResponseBase(LcCalcResponseBase):
    request: SafetyFactorCalcRequestBase
    safety_factor: float
    satisfactory: bool


class PayloadCalcResponseBase(LcCalcResponseBase):
    request: PayloadCalcRequestBase
    payload: float


class PayloadCalcResponse(BaseModel):
    request: PayloadCalcRequest
    base_responses: list[PayloadCalcResponseBase]


class SafetyFactorCalcResponse(BaseModel):
    request: SafetyFactorCalcRequest
    base_responses: list[SafetyFactorCalcResponseBase]
