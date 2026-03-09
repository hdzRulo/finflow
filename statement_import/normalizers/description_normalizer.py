"""Description cleanup and enrichment helpers."""


class DescriptionNormalizer:
    """Standardize whitespace and casing for descriptions."""

    def normalize(self, value: str | None) -> str:
        return (value or "").strip()
