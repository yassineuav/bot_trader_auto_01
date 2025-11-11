from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, validator


class SymbolImpact(BaseModel):
    symbol: str
    impact_pct: float = Field(ge=-100, le=100)


class NewsLLMResponse(BaseModel):
    label: str
    positive_pct: int = Field(ge=0, le=100)
    negative_pct: int = Field(ge=0, le=100)
    crowd_reaction: str
    trend: dict
    symbol_impacts: List[SymbolImpact]

    @validator("trend")
    def validate_trend(cls, v: dict) -> dict:
        direction = v.get("direction")
        if direction not in {"bullish", "bearish", "neutral"}:
            raise ValueError("Invalid trend direction")
        strength = v.get("strength_pct")
        if strength is None or not (0 <= strength <= 100):
            raise ValueError("Invalid trend strength")
        return v


class FallbackLLMResponse(BaseModel):
    market: str
    primary_driver: str
    direction: str
    strength_pct: int = Field(ge=0, le=100)

    @validator("direction")
    def validate_direction(cls, v: str) -> str:
        if v not in {"bullish", "bearish", "neutral"}:
            raise ValueError("Invalid direction")
        return v
