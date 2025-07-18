from sqlalchemy.orm import Session

from app.db.queries import get_crane_by_id
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
    crane = get_crane_by_id(db, request.crane_id)
    lc_table = crane.lc_table.get(request.boom_len)
    if lc_table is None:
        raise ValueError(
            f"No lifting capacity data found for boom length {request.boom_len}"
        )

    radius = request.radius
    if lc_table.get(radius) is not None:
        return LcCalcResponseBase(
            request=request, lifting_capacity=lc_table.get(radius)
        )

    nearest_lesser = get_nearest_lesser(radius, lc_table.keys())
    nearest_greater = get_nearest_greater(radius, lc_table.keys())

    if nearest_lesser is None or nearest_greater is None:
        raise ValueError(f"No lifting capacity data found for radius {radius}")

    lc_less = lc_table.get(nearest_lesser)
    lc_greater = lc_table.get(nearest_greater)

    lc = interpolate_1d(
        radius, nearest_lesser, lc_less, nearest_greater, lc_greater
    )

    return LcCalcResponseBase(request=request, lifting_capacity=lc)


def calc_payload_from_safety_factor(db: Session, request: PayloadCalcRequest):
    responses = []
    for req in request.base_requests:
        lc = calc_lc_base(db, req)
        payload = lc / req.safety_factor - req.equipment_weight
        responses.append(PayloadCalcResponseBase(request=req, payload=payload))

    return PayloadCalcResponse(request=request, responses=responses)


def calc_safety_factor_from_payload(
    db: Session, request: SafetyFactorCalcRequest
):
    responses = []
    for req in request.base_requests:
        lc = calc_lc_base(db, req)
        safety_factor = lc / (req.payload + req.equipment_weight)
        satisfactory = safety_factor >= MIN_SAFETY_FACTOR
        responses.append(
            SafetyFactorCalcResponseBase(
                request=req,
                safety_factor=safety_factor,
                satisfactory=satisfactory,
            )
        )

    return SafetyFactorCalcResponse(request=request, responses=responses)
