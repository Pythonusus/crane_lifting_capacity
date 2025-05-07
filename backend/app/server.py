import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import (
    CalculationRequest,
    CalculationResponse,
)

# Define absolute path to project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define absolute path to frontend directories
FRONTEND_DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")
FRONTEND_ASSETS_DIR = os.path.join(BASE_DIR, "frontend", "dist", "assets")

app = FastAPI(
    title="Crane Lifting Capacity API",
    description="FastAPI backend for the crane_lifting_capacity application",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/dist", StaticFiles(directory=FRONTEND_DIST_DIR), name="dist")
app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="assets")

# Set up templates
templates = Jinja2Templates(directory=FRONTEND_DIST_DIR)


@app.get("/")
def serve_react_app(request: Request):
    """Serve the React frontend application"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
def process(calculation: CalculationRequest):
    """
    Add two numbers and return the result

    Args:
        calculation: The request body containing the two numbers to add

    Returns:
        JSON response with the sum of the two numbers
    """
    result = calculation.first_number + calculation.second_number
    return CalculationResponse(
        result=result,
        first_number=calculation.first_number,
        second_number=calculation.second_number,
    )
