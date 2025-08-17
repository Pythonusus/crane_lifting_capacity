from pydantic import BaseModel, Field, field_validator


class LcCalcRequest(BaseModel):
    """
    Calculate crane lifting capacity for given crane, boom length and radius.
    """
    crane_name: str
    boom_len: str
    radius: str  # in meters, accepts string but validates as positive number

    @field_validator('radius')
    @classmethod
    def validate_radius(cls, radius: str):
        try:
            radius_float = float(radius)
            if radius_float <= 0:
                raise ValueError('Radius must be greater than 0')
            return radius
        except (ValueError, TypeError):
            raise ValueError('Radius must be a valid positive number')


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
