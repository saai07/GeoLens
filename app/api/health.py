"""Health and cache monitoring endpoints."""

from fastapi import APIRouter

from app.core.cache import get_cache_stats
from app.core.config import get_settings
from app.schemas.audit import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get("/cache-stats")
async def cache_stats() -> dict:
    return get_cache_stats()
