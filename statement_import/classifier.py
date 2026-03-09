"""Statement classifier interfaces and default implementation."""

from abc import ABC, abstractmethod

from statement_import.matchers.bank_detector import BankDetector
from statement_import.matchers.layout_detector import LayoutDetector


class BaseClassifier(ABC):
    """Classifies statement metadata for parser routing."""

    @abstractmethod
    def classify(self, extracted_payload: dict) -> dict:
        """Return hints such as bank_name, layout_family, and confidence."""


class HeuristicClassifier(BaseClassifier):
    """Keyword and layout based classifier."""

    def __init__(self) -> None:
        self.bank_detector = BankDetector()
        self.layout_detector = LayoutDetector()

    def classify(self, extracted_payload: dict) -> dict:
        text = extracted_payload.get("text") or extracted_payload.get("ocr_text") or ""
        bank = self.bank_detector.detect(text)
        layout = self.layout_detector.detect(extracted_payload)
        confidence = 0.9 if bank != "unknown" else 0.4
        return {"bank_name": bank, "layout_family": layout, "confidence": confidence}
