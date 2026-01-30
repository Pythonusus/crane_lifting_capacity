from pydantic import BaseModel

from app.schemas.calc_requests import (
    PayloadCalcRequest,
    SafetyFactorCalcRequest,
)


class LcCalcResponse(BaseModel):
    lifting_capacity: float


class SafetyFactorCalcResponse(LcCalcResponse):
    request: SafetyFactorCalcRequest
    safety_factor: float


class PayloadCalcResponse(LcCalcResponse):
    request: PayloadCalcRequest
    payload: float
