import uvicorn

from app.settings import PORT


def main():
    uvicorn.run("app.api:app", host="0.0.0.0", port=PORT, reload=True)


if __name__ == "__main__":
    main()
