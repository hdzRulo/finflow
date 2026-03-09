"""Transaction domain services."""

from sqlalchemy.orm import Session

from app import crud


def get_recent_transactions(db: Session, limit: int = 100):
    """Return recent transactions with optional limit."""
    return crud.list_transactions(db, limit=limit)
