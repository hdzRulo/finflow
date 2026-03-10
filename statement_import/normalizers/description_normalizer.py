"""Description cleanup and enrichment helpers."""

import re


class DescriptionNormalizer:
    """Standardize whitespace and casing for descriptions."""

    def normalize(self, value: str | None) -> str:
        cleaned = re.sub(r"\s+", " ", (value or "").strip())
        return cleaned
