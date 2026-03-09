"""Date normalization utilities."""

from datetime import date


class DateNormalizer:
    """Normalize date strings from multiple bank formats."""

    def normalize(self, value) -> date | None:
        if isinstance(value, date):
            return value
        return None
