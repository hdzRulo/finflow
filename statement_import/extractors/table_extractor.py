"""Table extractor backed by upstream reader output."""

from statement_import.extractors.base_extractor import BaseExtractor


class TableExtractor(BaseExtractor):
    """Extract structured table rows where available."""

    def extract(self, payload: dict) -> dict:
        payload.setdefault("tables", [])
        return payload
