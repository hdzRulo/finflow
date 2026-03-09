"""Pydantic schemas for API contracts and service payloads."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    kind: str = "expense"


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TransactionBase(BaseModel):
    account_id: int | None = None
    statement_id: int
    transaction_date: date
    posting_date: date | None = None
    description: str
    amount: Decimal
    currency: str = "USD"
    transaction_type: str = "expense"
    balance: Decimal | None = None
    category_id: int | None = None
    merchant: str | None = None
    reference_number: str | None = None
    source_file: str
    raw_text: str | None = None
    fingerprint_hash: str


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StatementImportCreate(BaseModel):
    source_file: str
    bank_name: str | None = None


class StatementImportRead(BaseModel):
    id: int
    source_file: str
    bank_name: str | None = None
    status: str
    total_rows_detected: int
    total_rows_imported: int
    total_rows_skipped: int
    report_json: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AccountBase(BaseModel):
    name: str
    institution: str | None = None
    account_number_masked: str | None = None
    currency: str = "USD"


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
