"""In-memory TTL cache for audit results. Swap to Redis for production scale."""

import hashlib
import json
import logging

from cachetools import TTLCache

logger = logging.getLogger(__name__)

# 500 URLs max, 24h TTL
_cache: TTLCache = TTLCache(maxsize=500, ttl=86400)


def _make_key(url: str) -> str:
    """Normalize and hash a URL into a fixed-length cache key."""
    normalized = url.lower().strip().rstrip("/")
    return hashlib.sha256(normalized.encode()).hexdigest()


def get_cached_result(url: str) -> dict | None:
    """Look up a cached audit result. Returns None on miss."""
    key = _make_key(url)
    result = _cache.get(key)
    if result is not None:
        logger.info("Cache HIT for %s", url)
        return json.loads(result)
    logger.info("Cache MISS for %s", url)
    return None


def set_cached_result(url: str, result: dict) -> None:
    """Store an audit result in the cache."""
    key = _make_key(url)
    _cache[key] = json.dumps(result)
    logger.info("Cached result for %s (TTL: 24h)", url)


def get_cache_stats() -> dict:
    """Current cache size, max capacity, and TTL."""
    return {
        "current_size": len(_cache),
        "max_size": _cache.maxsize,
        "ttl_seconds": int(_cache.ttl),
    }
