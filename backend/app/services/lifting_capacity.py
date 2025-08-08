"""
This module contains the functions for calculating the lifting capacity
and payload of a crane.
"""

from sqlalchemy.orm import Session

from app.db.queries import get_crane_by_name
from app.schemas.calc_requests import (
    LcCalcRequestBase,
    PayloadCalcRequest,
    SafetyFactorCalcRequest,
)
from app.schemas.calc_responses import (
    LcCalcResponseBase,
    PayloadCalcResponse,
    PayloadCalcResponseBase,
    SafetyFactorCalcResponse,
    SafetyFactorCalcResponseBase,
)
from app.settings import MIN_SAFETY_FACTOR
from utils.math import get_nearest_greater, get_nearest_lesser, interpolate_1d


def calc_lc_base(db: Session, request: LcCalcRequestBase) -> LcCalcResponseBase:
    """
    Calculate the lifting capacity of a crane
    based on the boom length and radius.
    """
    crane = get_crane_by_name(db, request.crane_name)
    lc_table = crane.lc_table.get(request.boom_len)
    if lc_table is None:
        raise ValueError(
            f"No lifting capacity data found for boom length {request.boom_len}"
        )

    # Create a mapping from float values to original string keys.
    # This is necessary because keys are strings, but we need to use them
    # as floats for finding nearest values. And then we need to convert them
    # back to strings to use as keys in lc_table.
    lc_table_keys_float_to_str_map = {float(k): k for k in lc_table.keys()}
    lc_table_keys_floats = list(lc_table_keys_float_to_str_map.keys())

    radius = request.radius
    if lc_table.get(radius) is not None:
        return LcCalcResponseBase(
            request=request, lifting_capacity=lc_table.get(radius)
        )

    nearest_lesser = get_nearest_lesser(float(radius), lc_table_keys_floats)
    nearest_greater = get_nearest_greater(float(radius), lc_table_keys_floats)

    if nearest_lesser is None or nearest_greater is None:
        raise ValueError(f"No lifting capacity data found for radius {radius}")

    # Use the original string keys from the mapping
    lc_less = lc_table.get(lc_table_keys_float_to_str_map[nearest_lesser])
    lc_greater = lc_table.get(lc_table_keys_float_to_str_map[nearest_greater])

    lc = interpolate_1d(
        float(radius), nearest_lesser, lc_less, nearest_greater, lc_greater
    )

    return LcCalcResponseBase(request=request, lifting_capacity=lc)


def calc_payload_from_safety_factor(db: Session, request: PayloadCalcRequest):
    """
    Calculate the payload of a crane
    based on the lifting capacity and safety factor.
    """
    responses = []
    for req in request.base_requests:
        lc = calc_lc_base(db, req).lifting_capacity
        payload = lc / req.safety_factor - req.equipment_weight
        responses.append(
            PayloadCalcResponseBase(
                request=req, lifting_capacity=lc, payload=payload
            )
        )

    return PayloadCalcResponse(request=request, base_responses=responses)


def calc_safety_factor_from_payload(
    db: Session, request: SafetyFactorCalcRequest
):
    """
    Calculate the safety factor of a crane
    based on the lifting capacity and payload.
    """
    responses = []
    for req in request.base_requests:
        lc = calc_lc_base(db, req).lifting_capacity
        safety_factor = lc / (req.payload + req.equipment_weight)
        satisfactory = safety_factor >= MIN_SAFETY_FACTOR
        responses.append(
            SafetyFactorCalcResponseBase(
                request=req,
                lifting_capacity=lc,
                safety_factor=safety_factor,
                satisfactory=satisfactory,
            )
        )

    return SafetyFactorCalcResponse(request=request, base_responses=responses)
