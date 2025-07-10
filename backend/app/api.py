from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import app.settings as settings
from app.db.queries import get_cranes_by_filters, get_manufacturers_from_db
from app.db.session import get_db
from app.schemas.calc_requests import (
    PayloadCalcRequest,
    SafetyFactorCalcRequest,
)
from app.schemas.cranes import ChassisTypesResponse, Crane, CraneFilterRequest
from app.services.lifting_capacity import (
    calc_payload_from_safety_factor,
    calc_safety_factor_from_payload,
)

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Mount frontend static files
app.mount(
    "/dist",
    StaticFiles(directory=settings.FRONTEND_DIST_PATH),
    name="dist",
)

# Set up templates
templates = Jinja2Templates(directory=settings.FRONTEND_DIST_PATH)


@app.get("/")
def serve_frontend(request: Request):
    """Serve the frontend app"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthcheck")
def healthcheck():
    """Check application status"""
    return {
        "status_code": 200,
        "message": f"{settings.APP_TITLE} app is up and running!",
    }


@app.post("/process")
def process(
    payload_request: PayloadCalcRequest | None = None,
    safety_request: SafetyFactorCalcRequest | None = None,
):
    """
    Process lifting capacity calculation requests.
    Supports both single and batch calculations for:
    - Payload calculation (given safety factor)
    - Safety factor calculation (given payload)
    """
    if payload_request:
        return calc_payload_from_safety_factor(payload_request)

    if safety_request:
        return calc_safety_factor_from_payload(safety_request)

    raise HTTPException(
        status_code=400,
        detail="Either payload or safety factor calculation request \
                must be provided",
    )


@app.post("/cranes")
def filter_cranes(filters: CraneFilterRequest, db: Session = Depends(get_db)):
    """
    Filter cranes based on the provided filters.
    If no filters are provided, return all cranes.

    Args:
        filters: Dictionary containing filter criteria.

    Returns:
        List of cranes.
    """
    crane_models = get_cranes_by_filters(db, filters)
    # Convert database models to Pydantic models for proper serialization
    cranes = [Crane.model_validate(crane) for crane in crane_models]
    return {"cranes": cranes}


@app.get("/chassis-types")
def get_chassis_types():
    """Get all available chassis types"""
    return ChassisTypesResponse()


@app.get("/manufacturers")
def get_manufacturers(db: Session = Depends(get_db)):
    """Get all available manufacturers"""
    manufacturers = get_manufacturers_from_db(db)
    return {"manufacturers": manufacturers}
