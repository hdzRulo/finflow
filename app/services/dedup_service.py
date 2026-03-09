"""Deduplication helpers for imported transactions."""

from hashlib import sha256


def build_fingerprint(record: dict) -> str:
    """Create deterministic hash from canonical transaction fields."""
    key = "|".join(
        [
            str(record.get("transaction_date", "")),
            str(record.get("amount", "")),
            str(record.get("currency", "")),
            str(record.get("description", "")).strip().lower(),
            str(record.get("reference_number", "")),
        ]
    )
    return sha256(key.encode("utf-8")).hexdigest()


def mark_duplicates(records: list[dict]) -> list[dict]:
    """Attach `is_duplicate` key based on in-batch fingerprint collisions."""
    seen: set[str] = set()
    for record in records:
        fingerprint = record.get("fingerprint_hash") or build_fingerprint(record)
        record["fingerprint_hash"] = fingerprint
        record["is_duplicate"] = fingerprint in seen
        seen.add(fingerprint)
    return records
