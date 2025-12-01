"""
Settings for the backend application.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# APP Settings
APP_TITLE = "Crane Lifting Capacity"
APP_DESCRIPTION = "Lifting capacity calculator for cranes"
APP_VERSION = "0.1.0"

# Mode in which the application is running
# If DEVELOPMENT is not set, it defaults to false
DEVELOPMENT = os.getenv("DEVELOPMENT", "false").lower() == "true"

# License check settings for Midas license checker
LICENSE_CHECK = os.getenv("LICENSE_CHECK", "true").lower() == "true"

# Port Settings
PORT = int(os.getenv("PORT", "8000"))

# Absolute path to backend root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Absolute path to project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# CORS Settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
CORS_METHODS = os.getenv("CORS_METHODS", "*").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")

# Supported image content types
SUPPORTED_IMAGE_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
]

# Pagination Settings
PAGINATION_SIZE = os.getenv("PAGINATION_SIZE", "15")

# Frontend dist directory (used to mount frontend in production)
FRONTEND_DIST_PATH = PROJECT_ROOT / "frontend" / "dist"

# Database URL for prepopulated app.db.sqlite3 database
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'app.db.sqlite3'}"
)

# Directory containing parsable cranes data (used by dev_scripts)
CRANES_DIR = PROJECT_ROOT / "cranes"
