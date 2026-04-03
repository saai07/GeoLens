"""POST /audit — runs the full GEO audit pipeline."""

import asyncio
import logging

from fastapi import APIRouter, Request

from app.core.cache import get_cached_result, set_cached_result
from app.core.limiter import limiter
from app.core.llm import generate_schema
from app.core.scorer import run_scoring
from app.schemas.audit import AuditRequest, AuditResponse
from app.services.scraper import fetch_page, fetch_robots_txt, parse_page

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Audit"])


@router.post("/audit", response_model=AuditResponse)
@limiter.limit("10/minute")
async def run_audit(request: Request, body: AuditRequest) -> AuditResponse:
    """Run a full GEO audit on the provided URL."""
    url = str(body.url)
    logger.info("=== GEO Audit requested for %s ===", url)

    cached = get_cached_result(url)
    if cached:
        logger.info("Returning cached result for %s", url)
        return AuditResponse(**cached)

    (html, final_url), robots_txt = await asyncio.gather(
        fetch_page(url),
        fetch_robots_txt(url),
    )

    page_data, soup = parse_page(html)

    scoring_result, recommended_schema = await asyncio.gather(
        run_scoring(soup, robots_txt),
        generate_schema(page_data, final_url),
    )

    response = AuditResponse(
        url=final_url,
        geo_score=scoring_result["geo_score"],
        geo_grade=scoring_result["geo_grade"],
        metrics=scoring_result["metrics"],
        recommendations=scoring_result["recommendations"],
        recommended_schema=recommended_schema,
        page_title=page_data.get("title", ""),
        page_description=page_data.get("meta_description", ""),
        page_headings=page_data.get("headings", []),
        page_image=page_data.get("first_image", ""),
    )

    set_cached_result(url, response.model_dump())

    logger.info(
        "=== Audit complete: %s | %d/100 (%s) ===",
        final_url, response.geo_score, response.geo_grade,
    )
    return response
