import uvicorn

from app.settings import HOT_RELOAD, PORT


def main():
    # Start the FastAPI application with uvicorn
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=PORT,
        reload=HOT_RELOAD,  # Auto-reload only in development mode
    )


if __name__ == "__main__":
    main()
