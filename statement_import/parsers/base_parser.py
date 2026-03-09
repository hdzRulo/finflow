"""Base parser class for all bank statement parser plugins."""

from abc import ABC, abstractmethod


class BaseStatementParser(ABC):
    """Converts extracted statement payload into raw transaction dictionaries."""

    name = "base"

    @classmethod
    @abstractmethod
    def can_parse(cls, classification: dict) -> bool:
        pass

    @abstractmethod
    def parse(self, extracted_payload: dict) -> list[dict]:
        pass
