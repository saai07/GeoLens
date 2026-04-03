"""FastAPI app setup — logging, middleware, and router registration."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.audit import router as audit_router
from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Audit any public webpage for AI citation readiness. "
        "Scores across GEO metrics and generates a recommended JSON-LD schema "
        "using LLMs."
    ),
    version=settings.app_version,
    contact={"name": "Sai Prasana", "url": "https://github.com/saai07"},
    debug=settings.debug,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(health_router)
app.include_router(audit_router)

logger.info("GeoLens API started — version %s", settings.app_version)
