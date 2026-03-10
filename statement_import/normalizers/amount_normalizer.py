"""Amount normalization utilities."""

from decimal import Decimal, InvalidOperation


class AmountNormalizer:
    """Convert source amounts into canonical Decimal values."""

    def normalize(self, value, tx_type: str | None = None) -> Decimal:
        raw = str(value or "0").replace(",", "").replace("$", "").strip()
        sign = -1 if "(" in raw and ")" in raw else 1
        raw = raw.replace("(", "").replace(")", "")
        try:
            dec = Decimal(raw) * sign
        except InvalidOperation:
            dec = Decimal("0")

        if tx_type == "expense" and dec > 0:
            dec = -dec
        elif tx_type == "income" and dec < 0:
            dec = abs(dec)
        return dec
