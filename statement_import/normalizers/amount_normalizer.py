"""Amount normalization utilities."""

from decimal import Decimal


class AmountNormalizer:
    """Convert source amounts into canonical Decimal values."""

    def normalize(self, value) -> Decimal:
        try:
            return Decimal(str(value))
        except Exception:
            return Decimal("0")
