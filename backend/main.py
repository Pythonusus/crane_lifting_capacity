import uvicorn

from app.settings import DEVELOPMENT, PORT


def main():
    # Start the FastAPI application with uvicorn
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=PORT,
        reload=DEVELOPMENT,  # Auto-reload only in development mode
    )


if __name__ == "__main__":
    main()
