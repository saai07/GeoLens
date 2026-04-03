"""Pydantic models for API request/response validation."""

from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class AuditRequest(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="Public webpage URL to audit.",
        examples=["https://stripe.com"],
    )


class MetricResult(BaseModel):
    metric: str = Field(..., description="Name of the metric.")
    score: int = Field(..., ge=0, description="Points earned.")
    max_score: int = Field(..., gt=0, description="Maximum possible points.")
    status: Literal["pass", "partial", "fail"] = Field(
        ...,
        description="pass (≥80%), partial (≥40%), or fail (<40% of max).",
    )
    detail: str = Field(..., description="Explanation of what was found.")


class AuditResponse(BaseModel):
    """Complete audit result returned by POST /audit."""

    url: str = Field(..., description="The audited URL (after redirects).")
    geo_score: int = Field(..., ge=0, le=100, description="Total score out of 100.")
    geo_grade: Literal["A", "B", "C", "D", "F"] = Field(
        ..., description="Letter grade from geo_score."
    )
    metrics: list[MetricResult] = Field(
        ..., description="Breakdown of each scoring metric."
    )
    recommendations: list[str] = Field(
        ..., description="Top 3 actionable improvement suggestions."
    )
    recommended_schema: dict = Field(
        ..., description="Gemini-generated JSON-LD block ready to embed."
    )
    page_title: str = Field(default="")
    page_description: str = Field(default="")
    page_headings: list[dict[str, Any]] = Field(default_factory=list)
    page_image: str = Field(default="")


class HealthResponse(BaseModel):
    """Response for GET /health."""

    status: str = Field(default="healthy")
    service: str = Field(default="GeoLens Audit API")
    version: str = Field(default="1.0.0")
