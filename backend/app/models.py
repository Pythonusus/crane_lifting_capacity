from pydantic import BaseModel


class CalculationRequest(BaseModel):
    first_number: float
    second_number: float


class CalculationResponse(BaseModel):
    result: float
    first_number: float
    second_number: float
