"""Base extractor interface for statement payload extraction."""

from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Extracts intermediate payload (text/tables/metadata) from file output."""

    @abstractmethod
    def extract(self, payload: dict) -> dict:
        pass
