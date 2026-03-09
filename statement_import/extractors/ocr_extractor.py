"""OCR extractor wrapper that can enrich payload with OCR text."""

from statement_import.extractors.base_extractor import BaseExtractor
from statement_import.readers.ocr_reader import OCRReader


class OCRExtractor(BaseExtractor):
    """Fallback extractor for scanned statements."""

    def __init__(self) -> None:
        self.reader = OCRReader()

    def extract(self, payload: dict) -> dict:
        payload.setdefault("ocr_text", "")
        return payload
