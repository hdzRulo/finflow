"""Transaction API endpoints."""

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.dedup_service import build_fingerprint
from app.services.transaction_service import create_transaction, get_recent_transactions

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[schemas.TransactionRead])
def list_transactions(
    limit: int = Query(default=100, le=500),
    date_from: date | None = None,
    date_to: date | None = None,
    category_id: int | None = None,
    description: str | None = None,
    amount_min: Decimal | None = None,
    amount_max: Decimal | None = None,
    db: Session = Depends(get_db),
):
    return get_recent_transactions(
        db,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
        category_id=category_id,
        description=description,
        amount_min=amount_min,
        amount_max=amount_max,
    )


@router.post("", response_model=schemas.TransactionRead)
def create_transaction_endpoint(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    if not payload.fingerprint_hash:
        payload.fingerprint_hash = build_fingerprint(payload.model_dump())
    return create_transaction(db, payload)


@router.put("/{transaction_id}", response_model=schemas.TransactionRead)
def update_transaction_endpoint(transaction_id: int, payload: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    row = crud.get_transaction(db, transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud.update_transaction(db, row, payload)


@router.delete("/{transaction_id}")
def delete_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    row = crud.get_transaction(db, transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    crud.delete_transaction(db, row)
    return {"status": "deleted"}
