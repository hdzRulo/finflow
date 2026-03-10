"""Transaction domain services."""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app import crud, schemas


def get_recent_transactions(
    db: Session,
    *,
    limit: int = 100,
    date_from: date | None = None,
    date_to: date | None = None,
    category_id: int | None = None,
    description: str | None = None,
    amount_min: Decimal | None = None,
    amount_max: Decimal | None = None,
):
    return crud.list_transactions(
        db,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
        category_id=category_id,
        description=description,
        amount_min=amount_min,
        amount_max=amount_max,
    )


def create_transaction(db: Session, payload: schemas.TransactionCreate):
    return crud.create_transaction(db, payload)
