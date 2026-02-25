"""Script for checking status of cranes URLs"""

import asyncio
from typing import Optional

import aiohttp
from pydantic import HttpUrl, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import CraneDbModel
from app.settings import DATABASE_URL

# Headers used for HTTP requests (browser-like, avoid blocking)
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

REQUEST_TIMEOUT = 10
MAX_CONCURRENT = 20


def is_valid_url(url: str) -> bool:
    try:
        HttpUrl(url)
        return True
    except ValidationError:
        return False


async def _check_one_url(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    url: str,
) -> tuple[str, str]:
    """
    Check a single URL. Returns (url, status) where status is
    'ok', 'invalid', or 'unreachable'.
    """
    if not is_valid_url(url):
        return (url, "invalid")
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return (url, "ok")
                return (url, "unreachable")
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return (url, "unreachable")


async def _check_all_urls(unique_urls: set[str]) -> tuple[list[str], list[str]]:
    invalid_urls: list[str] = []
    unreachable_urls: list[str] = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async with aiohttp.ClientSession(headers=REQUEST_HEADERS) as session:
        tasks = [
            _check_one_url(session, semaphore, url) for url in unique_urls
        ]
        for coro in asyncio.as_completed(tasks):
            url, status = await coro
            print(f"URL: {url}")
            if status == "ok":
                print("URL is reachable!\n")
            elif status == "invalid":
                invalid_urls.append(url)
                print("URL is not valid!\n")
            else:
                unreachable_urls.append(url)
                print("URL is not reachable!\n")

    return invalid_urls, unreachable_urls


def check_cranes_urls(
    database_url: Optional[str] = None,
) -> None:
    """
    Gathers all cranes URL from DB.
    Manufacturer URL, Crane URL, DWG URL.
    Checks if the URLs are valid.
    Sends test requests to check if they are reachable.
    Prints the results.
    """
    final_database_url = database_url or DATABASE_URL
    if not final_database_url:
        print(
            "Error: DATABASE_URL must be provided via argument or in settings"
        )
        return

    print(f"Using database URL: {final_database_url}")

    engine = create_engine(final_database_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        url_groups = session.query(
            CraneDbModel.manufacturer_url,
            CraneDbModel.crane_url,
            CraneDbModel.dwg_url,
        ).all()
        print(f"\nFound {len(url_groups)} url_groups in database:")
        unique_urls = set()
        for url_group in url_groups:
            for url in (
                url_group.manufacturer_url,
                url_group.crane_url,
                url_group.dwg_url,
            ):
                if url:
                    unique_urls.add(url)
        print(f"\nFound {len(unique_urls)} unique URLs in database:")
        print("\n" + "=" * 80 + "\n")

        invalid_urls, unreachable_urls = asyncio.run(
            _check_all_urls(unique_urls)
        )

        print("\n" + "=" * 80 + "\n")
        if invalid_urls or unreachable_urls:
            print(f"{len(invalid_urls)} are invalid!")
            print(f"{len(unreachable_urls)} are unreachable!")
        else:
            print("All URLS are OK!")

    finally:
        session.close()
