"""Date normalization utilities."""

from datetime import date, datetime


class DateNormalizer:
    """Normalize date strings from multiple bank formats."""

    FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"]

    def normalize(self, value) -> date | None:
        if isinstance(value, date):
            return value
        if not value:
            return None
        raw = str(value).strip()
        for fmt in self.FORMATS:
            try:
                return datetime.strptime(raw, fmt).date()
            except ValueError:
                continue
        return None
