"""CRUD helpers for domain entities."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_category(db: Session, payload: schemas.CategoryCreate) -> models.Category:
    category = models.Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories(db: Session) -> list[models.Category]:
    return list(db.scalars(select(models.Category).order_by(models.Category.name)).all())


def list_transactions(db: Session, limit: int = 100) -> list[models.Transaction]:
    stmt = select(models.Transaction).order_by(models.Transaction.transaction_date.desc()).limit(limit)
    return list(db.scalars(stmt).all())


def create_statement_import(db: Session, payload: schemas.StatementImportCreate) -> models.StatementImport:
    item = models.StatementImport(source_file=payload.source_file, bank_name=payload.bank_name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
