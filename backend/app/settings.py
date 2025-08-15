"""
Settings for the backend application.

FRONTEND_DIST_URL and DATABASE_URL are loaded from environment variables.
See .env.example for more information.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# APP Settings
APP_TITLE = "Crane Lifting Capacity"
APP_DESCRIPTION = "FastAPI backend for the crane_lifting_capacity application"
APP_VERSION = "0.1.0"

# Absolute path to backend root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Frontend dist directory
FRONTEND_DIST_PATH = (
    os.getenv("FRONTEND_DIST_PATH") or BASE_DIR.parent / "frontend" / "dist"
)

# Database Settings
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or f"sqlite:///{BASE_DIR / 'data' / 'app.db.sqlite3'}"
)

# Data directory
ATTACHMENTS_DIR = Path(os.getenv("ATTACHMENTS_DIR") or BASE_DIR / "attachments")

# Port Settings
PORT = int(os.getenv("PORT", "8000"))

# Development mode
DEVELOPMENT = os.getenv("DEVELOPMENT", "false").lower() == "true"


# CORS Settings
# DO NOT PASS CORS SETTINGS FROM ENV VARIABLES
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Supported image content types
SUPPORTED_IMAGE_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
]

# Pagination Settings
DEFAULT_PAGE_SIZE = 15
