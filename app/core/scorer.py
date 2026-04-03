"""Rule-based scoring engine — 5 deterministic GEO metrics, no LLM."""

import json
import logging
import re

from bs4 import BeautifulSoup

from app.schemas.audit import MetricResult

logger = logging.getLogger(__name__)

VAGUE_HEADING_WORDS = {
    "details", "more info", "click here", "read more", "learn more",
    "info", "stuff", "things", "misc", "other", "untitled",
}
AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot"]


def _status_from_ratio(score: int, max_score: int) -> str:
    """Map score ratio to pass/partial/fail."""
    ratio = score / max_score if max_score > 0 else 0
    if ratio >= 0.8:
        return "pass"
    elif ratio >= 0.4:
        return "partial"
    return "fail"


def score_schema_markup(soup: BeautifulSoup) -> MetricResult:
    """Score JSON-LD structured data presence and quality (max 25 pts)."""
    max_score = 25
    score = 0
    details = []

    ld_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    if not ld_scripts:
        return MetricResult(
            metric="Schema Markup", score=0, max_score=max_score,
            status="fail", detail="No JSON-LD script tag found.",
        )

    score += 7
    details.append("JSON-LD script tag found.")

    all_ld = []
    for script in ld_scripts:
        try:
            data = json.loads(script.string or "")
            all_ld.extend(data if isinstance(data, list) else [data])
        except (json.JSONDecodeError, TypeError):
            continue

    if not all_ld:
        details.append("JSON-LD content could not be parsed.")
        return MetricResult(
            metric="Schema Markup", score=score, max_score=max_score,
            status=_status_from_ratio(score, max_score), detail=" ".join(details),
        )

    has_type = any(d.get("@type") for d in all_ld if isinstance(d, dict))
    if has_type:
        score += 6
        types_found = [str(d.get("@type")) for d in all_ld if isinstance(d, dict) and d.get("@type")]
        details.append(f"Valid @type found: {', '.join(types_found[:3])}.")
    else:
        details.append("No @type field in JSON-LD.")

    has_name = any(d.get("name") for d in all_ld if isinstance(d, dict))
    has_desc = any(d.get("description") for d in all_ld if isinstance(d, dict))
    if has_name and has_desc:
        score += 6
        details.append("'name' and 'description' fields present.")
    elif has_name:
        score += 3
        details.append("'name' present but 'description' missing.")
    elif has_desc:
        score += 3
        details.append("'description' present but 'name' missing.")
    else:
        details.append("Neither 'name' nor 'description' found.")

    has_url = any(d.get("url") for d in all_ld if isinstance(d, dict))
    has_image = any(d.get("image") for d in all_ld if isinstance(d, dict))
    if has_url and has_image:
        score += 6
        details.append("'url' and 'image' fields present.")
    elif has_url:
        score += 3
        details.append("'url' present but 'image' missing.")
    elif has_image:
        score += 3
        details.append("'image' present but 'url' missing.")
    else:
        details.append("Neither 'url' nor 'image' found.")

    logger.info("Schema Markup: %d/%d", score, max_score)
    return MetricResult(
        metric="Schema Markup", score=score, max_score=max_score,
        status=_status_from_ratio(score, max_score), detail=" ".join(details),
    )


def score_semantic_html(soup: BeautifulSoup) -> MetricResult:
    """Score use of semantic HTML5 elements (max 20 pts). 5 each for main/article/section/nav."""
    max_score = 20
    score = 0
    found, missing = [], []

    for tag in ["main", "article", "section", "nav"]:
        if soup.find(tag):
            score += 5
            found.append(f"<{tag}>")
        else:
            missing.append(f"<{tag}>")

    parts = []
    if found:
        parts.append(f"Found: {', '.join(found)}.")
    if missing:
        parts.append(f"Missing: {', '.join(missing)}.")

    logger.info("Semantic HTML: %d/%d", score, max_score)
    return MetricResult(
        metric="Semantic HTML", score=score, max_score=max_score,
        status=_status_from_ratio(score, max_score), detail=" ".join(parts),
    )


def score_image_alt_text(soup: BeautifulSoup) -> MetricResult:
    """Score alt text coverage on <img> tags (max 20 pts)."""
    max_score = 20
    images = soup.find_all("img")
    total = len(images)

    if total == 0:
        return MetricResult(
            metric="Image Alt Text", score=max_score, max_score=max_score,
            status="pass", detail="No images found; alt text check not applicable.",
        )

    with_alt = sum(1 for img in images if img.get("alt", "").strip())
    without_alt = total - with_alt
    percentage = (with_alt / total) * 100
    score = round((with_alt / total) * max_score)

    detail = f"{with_alt}/{total} images ({percentage:.0f}%) have non-empty alt text."
    if without_alt:
        detail += f" {without_alt} image(s) missing alt."

    logger.info("Image Alt Text: %d/%d", score, max_score)
    return MetricResult(
        metric="Image Alt Text", score=score, max_score=max_score,
        status=_status_from_ratio(score, max_score), detail=detail,
    )


def score_content_structure(soup: BeautifulSoup) -> MetricResult:
    """Score heading hierarchy quality (max 20 pts). Checks h1 count, h2/h3 usage, level skips, vague text."""
    max_score = 20
    score = 0
    details = []

    h1s = soup.find_all("h1")
    h2s = soup.find_all("h2")
    h3s = soup.find_all("h3")

    if len(h1s) == 1:
        score += 4
        details.append("Exactly one <h1>.")
    elif len(h1s) == 0:
        details.append("No <h1> found.")
    else:
        details.append(f"{len(h1s)} <h1> tags found (should be exactly 1).")

    if len(h2s) >= 2:
        score += 4
        details.append(f"{len(h2s)} <h2> tags (≥2 required).")
    elif len(h2s) == 1:
        score += 2
        details.append("Only 1 <h2>; at least 2 recommended.")
    else:
        details.append("No <h2> tags found.")

    if len(h3s) >= 1:
        score += 4
        details.append(f"{len(h3s)} <h3> tag(s) found.")
    else:
        details.append("No <h3> tags found.")

    all_headings = soup.find_all(re.compile(r"^h[1-6]$"))
    levels = [int(h.name[1]) for h in all_headings]
    skipped = any(
        levels[i] > levels[i - 1] + 1
        for i in range(1, len(levels))
    )
    if not skipped:
        score += 4
        details.append("No skipped heading levels.")
    else:
        details.append("Skipped heading levels detected (e.g., h1 → h3).")

    heading_texts = [h.get_text(strip=True).lower() for h in soup.find_all(["h1", "h2", "h3"])]
    vague = [t for t in heading_texts if t in VAGUE_HEADING_WORDS]
    if not vague:
        score += 4
        details.append("All headings are descriptive.")
    else:
        details.append(f"Vague heading(s): {', '.join(repr(v) for v in vague[:3])}.")

    logger.info("Content Structure: %d/%d", score, max_score)
    return MetricResult(
        metric="Content Structure", score=score, max_score=max_score,
        status=_status_from_ratio(score, max_score), detail=" ".join(details),
    )


def score_ai_bot_access(robots_txt: str) -> MetricResult:
    """Score whether AI crawlers (GPTBot, ClaudeBot, PerplexityBot) are allowed (max 15 pts)."""
    max_score = 15
    score = 0
    allowed, blocked = [], []

    robots_lower = robots_txt.lower()

    for bot in AI_BOTS:
        bot_lower = bot.lower()
        is_blocked = False
        blocks = re.split(r"(?i)user-agent\s*:", robots_lower)

        for block in blocks:
            block_stripped = block.strip()
            if block_stripped.startswith(bot_lower) or block_stripped.startswith("*"):
                if block_stripped.startswith("*") and any(
                    b.strip().startswith(bot_lower) for b in blocks if b.strip()
                ):
                    continue
                for line in block_stripped.split("\n")[1:]:
                    line = line.strip()
                    if line.startswith("disallow") and ":" in line:
                        path = line.split(":", 1)[1].strip()
                        if path in ("/", "/*"):
                            is_blocked = True
                            break
                if is_blocked:
                    break

        if is_blocked:
            blocked.append(bot)
        else:
            score += 5
            allowed.append(bot)

    if not robots_txt.strip():
        return MetricResult(
            metric="AI Bot Access", score=max_score, max_score=max_score,
            status="pass", detail="No robots.txt found; all AI bots assumed allowed.",
        )

    parts = []
    if allowed:
        parts.append(f"Allowed: {', '.join(allowed)}.")
    if blocked:
        parts.append(f"Blocked: {', '.join(blocked)}. Update robots.txt to allow them.")

    logger.info("AI Bot Access: %d/%d", score, max_score)
    return MetricResult(
        metric="AI Bot Access", score=score, max_score=max_score,
        status=_status_from_ratio(score, max_score), detail=" ".join(parts),
    )


def compute_geo_grade(score: int) -> str:
    """A (≥80), B (≥60), C (≥40), D (≥20), F (<20)."""
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    if score >= 20:
        return "D"
    return "F"


def generate_recommendations(metrics: list[MetricResult]) -> list[str]:
    """Return top 3 actionable recommendations, sorted by weakest metric first."""
    recommendation_map = {
        "Schema Markup": (
            "Add a complete JSON-LD block with @type, name, description, url, and image. "
            "This is the single most impactful change for AI citation readiness."
        ),
        "Semantic HTML": (
            "Wrap content in <main>, <article>, <section>, and <nav> elements. "
            "AI parsers rely on these to understand content structure."
        ),
        "Image Alt Text": (
            "Add descriptive alt attributes to every <img> tag. "
            "AI engines use alt text to understand and cite visual content."
        ),
        "Content Structure": (
            "Use exactly one <h1>, at least two <h2>s, and at least one <h3>. "
            "Avoid skipping heading levels and use specific, keyword-rich text."
        ),
        "AI Bot Access": (
            "Update robots.txt to allow GPTBot, ClaudeBot, and PerplexityBot. "
            "Blocking these crawlers prevents AI engines from indexing your content."
        ),
    }

    sorted_metrics = sorted(
        metrics,
        key=lambda m: m.score / m.max_score if m.max_score > 0 else 0,
    )

    return [
        recommendation_map.get(m.metric, f"Improve your {m.metric} score.")
        for m in sorted_metrics[:3]
    ]


async def run_scoring(soup: BeautifulSoup, robots_txt: str) -> dict:
    """Run all 5 metrics on a pre-parsed soup and return aggregated results."""
    metrics = [
        score_schema_markup(soup),
        score_semantic_html(soup),
        score_image_alt_text(soup),
        score_content_structure(soup),
        score_ai_bot_access(robots_txt),
    ]

    geo_score = sum(m.score for m in metrics)
    geo_grade = compute_geo_grade(geo_score)
    recommendations = generate_recommendations(metrics)

    logger.info("GEO Score: %d/100 (Grade: %s)", geo_score, geo_grade)
    return {
        "metrics": metrics,
        "geo_score": geo_score,
        "geo_grade": geo_grade,
        "recommendations": recommendations,
    }
