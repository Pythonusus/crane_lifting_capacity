"""
This module contains the API endpoints for the
Crane Lifting Capacity application.

The API provides endpoints for:
- Crane data management (filtering, retrieval)
- Lifting capacity calculations (payload and safety factor)
- Static file serving for frontend
- Health monitoring

API Structure:
├── /                    # Frontend application
├── /healthcheck        # Health monitoring
├── /process            # Lifting capacity calculations
├── /api/cranes         # Crane data endpoints
├── /api/chassis-types  # Chassis type enumeration
├── /api/manufacturers  # Manufacturer listing
├── /api/sort-options   # Sorting options
└── /api/attachments   # Attachment serving
"""

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import app.settings as settings
from app.db.queries import (
    get_crane_db_model_by_name,
    get_cranes_db_models_by_filters,
    get_filtered_cranes_count,
    get_manufacturers_from_db,
)
from app.db.session import get_db
from app.schemas.calc_requests import (
    PayloadCalcRequest,
    SafetyFactorCalcRequest,
)
from app.schemas.cranes import (
    ChassisTypesResponse,
    Crane,
    CraneFilterRequest,
    CraneListItem,
    CraneListResponse,
    SortOptionsResponse,
)
from app.services.crane_attachments import serve_attachment
from app.services.lifting_capacity import (
    calc_payload_from_safety_factor,
    calc_safety_factor_from_payload,
)

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)


@app.on_event("startup")
def startup_event():
    """Setup logging after app startup."""
    from app.logging_config import setup_logging
    setup_logging()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Mount frontend static files only when not in development mode
if not settings.DEVELOPMENT:
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


@app.get("/health")
def health():
    """Check application status"""
    return {
        "status_code": 200,
        "message": f"{settings.APP_TITLE} app is up and running!",
    }


@app.post("/process")
def process(
    payload_request: PayloadCalcRequest | None = None,
    safety_request: SafetyFactorCalcRequest | None = None,
    db: Session = Depends(get_db),
):
    """
    Process lifting capacity calculation requests.
    Supports both single and batch calculations for:
    - Payload calculation (given safety factor)
    - Safety factor calculation (given payload)
    """
    if payload_request:
        return calc_payload_from_safety_factor(db, payload_request)

    if safety_request:
        return calc_safety_factor_from_payload(db, safety_request)

    raise HTTPException(
        status_code=400,
        detail="Either payload or safety factor calc request must be provided",
    )


@app.post("/api/cranes/count")
def get_cranes_count(
    filters: CraneFilterRequest, db: Session = Depends(get_db)
):
    """
    Get the total count of cranes matching the provided filters.

    Args:
        filters: Dictionary containing filter criteria.

    Returns:
        Total count of cranes matching the filters.
    """
    cranes_count = get_filtered_cranes_count(db, filters)
    return {"cranes_count": cranes_count}


@app.post("/api/cranes")
def get_cranes(filters: CraneFilterRequest, db: Session = Depends(get_db)):
    """
    Filter cranes based on the provided filters with load-more pagination.
    If no filters are provided, return all cranes.

    Args:
        filters: Dictionary containing filter criteria and
                 offset/limit parameters.

    Returns:
        List of cranes with load-more metadata.
    """
    crane_models = get_cranes_db_models_by_filters(db, filters)
    cranes_count = get_filtered_cranes_count(db, filters)

    # Convert db models to simplified Pydantic models for better performance
    cranes = [CraneListItem.model_validate(crane) for crane in crane_models]

    # Calculate load-more metadata
    offset = filters.offset or 0
    returned_count = len(cranes)
    has_more = (offset + returned_count) < cranes_count

    return CraneListResponse(
        cranes=cranes,
        cranes_count=cranes_count,
        has_more=has_more,
        returned_count=returned_count,
    )


@app.get("/api/cranes/{crane_name}")
def get_crane_by_name(crane_name: str, db: Session = Depends(get_db)):
    """
    Get a single crane by name.

    Args:
        crane_name: Name of the crane to retrieve.

    Returns:
        The crane object.
    """
    crane_db_model = get_crane_db_model_by_name(db, crane_name)
    if not crane_db_model:
        raise HTTPException(status_code=404, detail="Crane not found")

    return Crane.model_validate(crane_db_model)


@app.get("/api/chassis-types")
def get_chassis_types():
    """Get all available chassis types"""
    return ChassisTypesResponse()


@app.get("/api/manufacturers")
def get_manufacturers(db: Session = Depends(get_db)):
    """Get all available manufacturers"""
    manufacturers = get_manufacturers_from_db(db)
    return {"manufacturers": manufacturers}


@app.get("/api/sort-options")
def get_sort_options():
    """Get all available sorting options"""
    return SortOptionsResponse()


@app.get("/api/attachments/{attachment_id}")
def serve_attachment_by_id(attachment_id: int, db: Session = Depends(get_db)):
    """
    Serve a crane attachment by its ID.
    """
    return serve_attachment(attachment_id, db)
