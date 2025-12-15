"""
This module contains the functions for calculating the lifting capacity
and payload of a crane.
"""

from sqlalchemy.orm import Session

from app.db.queries import get_crane_db_model_by_name
from app.schemas.calc_requests import (
    LcCalcRequest,
    PayloadCalcRequest,
    SafetyFactorCalcRequest,
)
from app.schemas.calc_responses import (
    LcCalcResponse,
    PayloadCalcResponse,
    SafetyFactorCalcResponse,
)
from utils.lifting_capacity import get_lifting_capacity_at_radius


def calc_lc_base(db: Session, request: LcCalcRequest) -> LcCalcResponse:
    """
    Calculate the lifting capacity of a crane
    based on the boom length and radius.
    """
    crane = get_crane_db_model_by_name(db, request.crane_name)
    if not crane:
        raise ValueError(f"Crane '{request.crane_name}' not found")

    lc_table = crane.lc_tables.get(request.table_name)["table"].get(
        request.boom_len
    )
    if lc_table is None:
        raise ValueError(
            f"No lifting capacity data found for boom length {request.boom_len}"
        )

    lifting_capacity = get_lifting_capacity_at_radius(lc_table, request.radius)
    if lifting_capacity is None:
        raise ValueError(
            f"No lifting capacity data found for radius {request.radius}"
        )

    return LcCalcResponse(lifting_capacity=lifting_capacity)


def calc_payload_from_safety_factor(db: Session, request: PayloadCalcRequest):
    """
    Calculate the payload of a crane
    based on the lifting capacity and safety factor.
    """
    lc_response = calc_lc_base(db, request)
    payload = (
        lc_response.lifting_capacity / request.safety_factor
        - request.equipment_weight
    )
    return PayloadCalcResponse(
        request=request,
        lifting_capacity=lc_response.lifting_capacity,
        payload=payload,
    )


def calc_safety_factor_from_payload(
    db: Session, request: SafetyFactorCalcRequest
):
    """
    Calculate the safety factor of a crane
    based on the lifting capacity and payload.
    """
    lc_response = calc_lc_base(db, request)
    safety_factor = lc_response.lifting_capacity / (
        request.payload + request.equipment_weight
    )
    return SafetyFactorCalcResponse(
        request=request,
        lifting_capacity=lc_response.lifting_capacity,
        safety_factor=safety_factor,
    )
