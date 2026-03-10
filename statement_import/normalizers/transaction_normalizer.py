"""Canonical transaction normalization for parser outputs."""

from app.services.dedup_service import build_fingerprint
from statement_import.normalizers.amount_normalizer import AmountNormalizer
from statement_import.normalizers.date_normalizer import DateNormalizer
from statement_import.normalizers.description_normalizer import DescriptionNormalizer


class TransactionNormalizer:
    """Normalize parser output to canonical transaction schema."""

    def __init__(self) -> None:
        self.date_normalizer = DateNormalizer()
        self.amount_normalizer = AmountNormalizer()
        self.description_normalizer = DescriptionNormalizer()

    def normalize(self, record: dict, file_path: str) -> dict:
        tx_type = record.get("transaction_type", "expense")
        normalized = {
            "account_id": record.get("account_id"),
            "statement_id": record.get("statement_id", 0),
            "transaction_date": self.date_normalizer.normalize(record.get("transaction_date")),
            "posting_date": self.date_normalizer.normalize(record.get("posting_date")),
            "description": self.description_normalizer.normalize(record.get("description")),
            "amount": self.amount_normalizer.normalize(record.get("amount", 0), tx_type),
            "currency": record.get("currency", "USD"),
            "transaction_type": tx_type,
            "balance": record.get("balance"),
            "category_id": record.get("category_id"),
            "merchant": record.get("merchant"),
            "reference_number": record.get("reference_number"),
            "source_file": file_path,
            "raw_text": record.get("raw_text"),
        }
        normalized["fingerprint_hash"] = build_fingerprint(normalized)
        return normalized
