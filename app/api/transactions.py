"""Transaction API endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TransactionRead
from app.services.transaction_service import get_recent_transactions

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
def list_transactions(limit: int = Query(default=100, le=500), db: Session = Depends(get_db)):
    """List transactions with basic pagination by limit."""
    return get_recent_transactions(db, limit=limit)
