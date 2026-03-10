"""CRUD helpers for domain entities."""

from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func, or_, select
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


def create_transaction(db: Session, payload: schemas.TransactionCreate) -> models.Transaction:
    row = models.Transaction(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_transaction(db: Session, transaction_id: int) -> models.Transaction | None:
    return db.get(models.Transaction, transaction_id)


def update_transaction(db: Session, row: models.Transaction, payload: schemas.TransactionUpdate) -> models.Transaction:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_transaction(db: Session, row: models.Transaction) -> None:
    db.delete(row)
    db.commit()


def list_transactions(
    db: Session,
    *,
    limit: int = 100,
    date_from: date | None = None,
    date_to: date | None = None,
    category_id: int | None = None,
    description: str | None = None,
    amount_min: Decimal | None = None,
    amount_max: Decimal | None = None,
) -> list[models.Transaction]:
    stmt = select(models.Transaction)
    conditions = []
    if date_from:
        conditions.append(models.Transaction.transaction_date >= date_from)
    if date_to:
        conditions.append(models.Transaction.transaction_date <= date_to)
    if category_id:
        conditions.append(models.Transaction.category_id == category_id)
    if description:
        like = f"%{description.strip()}%"
        conditions.append(or_(models.Transaction.description.ilike(like), models.Transaction.merchant.ilike(like)))
    if amount_min is not None:
        conditions.append(models.Transaction.amount >= amount_min)
    if amount_max is not None:
        conditions.append(models.Transaction.amount <= amount_max)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    stmt = stmt.order_by(models.Transaction.transaction_date.desc(), models.Transaction.id.desc()).limit(limit)
    return list(db.scalars(stmt).all())


def create_statement_import(db: Session, payload: dict) -> models.StatementImport:
    item = models.StatementImport(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_import_history(db: Session, limit: int = 100) -> list[models.StatementImport]:
    stmt = select(models.StatementImport).order_by(models.StatementImport.created_at.desc()).limit(limit)
    return list(db.scalars(stmt).all())


def fingerprint_exists(db: Session, fingerprint_hash: str) -> bool:
    stmt = select(func.count(models.Transaction.id)).where(models.Transaction.fingerprint_hash == fingerprint_hash)
    return (db.execute(stmt).scalar_one() or 0) > 0
