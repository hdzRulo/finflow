"""Text extractor implementation placeholder."""

from statement_import.extractors.base_extractor import BaseExtractor


class TextExtractor(BaseExtractor):
    """Ensure text payload exists for classifier/parser usage."""

    def extract(self, payload: dict) -> dict:
        payload.setdefault("text", "")
        return payload
