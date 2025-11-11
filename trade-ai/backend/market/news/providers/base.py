from __future__ import annotations

import abc
import datetime as dt
from typing import Iterable, List, Protocol


class RawArticle(Protocol):
    @property
    def url(self) -> str: ...


class NewsProvider(abc.ABC):
    name: str

    @abc.abstractmethod
    def fetch_since(self, since: dt.datetime) -> List[dict]:
        raise NotImplementedError


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, NewsProvider] = {}

    def register(self, provider: NewsProvider) -> None:
        self._providers[provider.name] = provider

    def list(self) -> Iterable[NewsProvider]:
        return self._providers.values()

    def get(self, name: str) -> NewsProvider | None:
        return self._providers.get(name)


registry = ProviderRegistry()
