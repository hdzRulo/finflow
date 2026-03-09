"""Statement classifier interfaces and default implementation."""

from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    """Classifies statement metadata for parser routing."""

    @abstractmethod
    def classify(self, extracted_payload: dict) -> dict:
        """Return hints such as bank_name, layout_family, and confidence."""


class HeuristicClassifier(BaseClassifier):
    """Simple keyword-based classifier placeholder."""

    def classify(self, extracted_payload: dict) -> dict:
        text = (extracted_payload.get("text") or "").lower()
        if "example bank a" in text:
            return {"bank_name": "ExampleBankA", "layout_family": "table", "confidence": 0.9}
        if "example bank b" in text:
            return {"bank_name": "ExampleBankB", "layout_family": "line", "confidence": 0.9}
        return {"bank_name": "unknown", "layout_family": "generic", "confidence": 0.2}
