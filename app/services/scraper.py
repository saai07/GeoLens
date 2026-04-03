"""Scraper — fetches pages and robots.txt, parses HTML into structured data."""

import logging
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from app.core.config import get_settings

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_http_client: httpx.AsyncClient | None = None


def _get_http_client() -> httpx.AsyncClient:
    """Lazy singleton for connection pooling."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        settings = get_settings()
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.scraper_timeout_seconds),
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
    return _http_client


async def fetch_page(url: str) -> tuple[str, str]:
    """Fetch a webpage's HTML. Returns (html, final_url after redirects)."""
    settings = get_settings()
    client = _get_http_client()
    try:
        response = await client.get(url)
        response.raise_for_status()
    except httpx.TimeoutException:
        logger.error("Timeout fetching %s", url)
        raise HTTPException(
            status_code=504,
            detail=f"Timed out after {settings.scraper_timeout_seconds}s fetching {url}.",
        )
    except httpx.ConnectError:
        logger.error("Connection failed for %s", url)
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to {url}. Check the URL and try again.",
        )
    except httpx.HTTPStatusError as exc:
        logger.error("HTTP %d from %s", exc.response.status_code, url)
        raise HTTPException(
            status_code=502,
            detail=f"Received HTTP {exc.response.status_code} from {url}.",
        )
    except httpx.HTTPError as exc:
        logger.error("HTTP error fetching %s: %s", url, exc)
        raise HTTPException(status_code=502, detail=f"Failed to fetch {url}: {exc}")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        raise HTTPException(
            status_code=422,
            detail=(
                f"URL returned non-HTML content (Content-Type: {content_type}). "
                "Only HTML pages can be audited."
            ),
        )

    logger.info("Fetched %s (%d bytes)", url, len(response.text))
    return response.text, str(response.url)


async def fetch_robots_txt(url: str) -> str:
    """Fetch robots.txt from the base domain. Returns empty string on failure."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    client = _get_http_client()

    try:
        response = await client.get(robots_url)
        if response.status_code == 200:
            logger.info("Fetched robots.txt from %s", robots_url)
            return response.text
        logger.info("robots.txt not found at %s (HTTP %d)", robots_url, response.status_code)
        return ""
    except httpx.HTTPError as exc:
        logger.warning("Could not fetch robots.txt from %s: %s", robots_url, exc)
        return ""


def parse_page(html: str) -> tuple[dict, BeautifulSoup]:
    """Parse HTML and extract title, meta description, headings, and first image."""
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = ""
    if meta_desc_tag and meta_desc_tag.get("content"):
        meta_description = meta_desc_tag["content"].strip()

    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append({"level": tag.name, "text": text})

    first_image = ""
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        first_image = og_image["content"].strip()
    else:
        first_img_tag = soup.find("img", src=True)
        if first_img_tag:
            first_image = first_img_tag["src"].strip()

    logger.info(
        "Parsed page: title=%r headings=%d has_image=%s",
        title[:60] if title else "(none)",
        len(headings),
        bool(first_image),
    )

    page_data = {
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "first_image": first_image,
    }
    return page_data, soup
