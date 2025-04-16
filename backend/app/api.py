from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import app.settings as settings

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
