from __future__ import annotations

import json
import logging
from typing import Iterable, List

import openai
from django.conf import settings

from market.db import models
from . import prompts, schemas

logger = logging.getLogger(__name__)


def _invoke_llm(prompt: str, content: str) -> dict:
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    attempts = 0
    while attempts < 3:
        attempts += 1
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
        )
        text = response.output[0].content[0].text if response.output else ""
        try:
            payload = json.loads(text)
            return payload
        except json.JSONDecodeError:
            logger.warning("LLM returned invalid JSON, retrying (%s)", attempts)
    raise ValueError("Unable to parse LLM response after retries")


def analyze_articles(articles: Iterable[models.Article]) -> List[models.Sentiment]:
    sentiments: List[models.Sentiment] = []
    for article in articles:
        payload = _invoke_llm(prompts.NEWS_ANALYSIS_PROMPT, article.body[:4000])
        data = schemas.NewsLLMResponse(**payload)
        sentiment = models.Sentiment.objects.create(
            article=article,
            pos_pct=data.positive_pct,
            neg_pct=data.negative_pct,
            label=data.label,
            llm_version=settings.OPENAI_MODEL,
            trend_bull_bear=data.trend["direction"],
            trend_strength_pct=data.trend["strength_pct"],
            crowd_reaction_text=data.crowd_reaction,
        )
        sentiments.append(sentiment)
    return sentiments


def fallback_market_driver() -> schemas.FallbackLLMResponse:
    payload = _invoke_llm(prompts.FALLBACK_PROMPT, "What is driving the market?")
    return schemas.FallbackLLMResponse(**payload)
