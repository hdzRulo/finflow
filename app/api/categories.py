"""Category API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.post("", response_model=schemas.CategoryRead)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, payload)
