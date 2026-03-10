from app.services.dedup_service import mark_duplicates


def test_mark_duplicates_flags_collisions_with_account():
    rows = [
        {"account_id": 1, "transaction_date": "2024-01-01", "description": "A", "amount": 10, "currency": "USD"},
        {"account_id": 1, "transaction_date": "2024-01-01", "description": "A", "amount": 10, "currency": "USD"},
    ]
    result = mark_duplicates(rows)
    assert result[0]["is_duplicate"] is False
    assert result[1]["is_duplicate"] is True
