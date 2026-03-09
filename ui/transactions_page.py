"""Transactions page with basic CRUD actions."""

from decimal import Decimal

from nicegui import ui

from app import crud
from app.database import SessionLocal
from app.schemas import TransactionCreate
from app.services.dedup_service import build_fingerprint


def render_transactions_page() -> None:
    ui.label("Transactions").classes("text-h4")
    search = ui.input("Search description")
    rows_table = ui.table(columns=[
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "date", "label": "Date", "field": "date"},
        {"name": "description", "label": "Description", "field": "description"},
        {"name": "amount", "label": "Amount", "field": "amount"},
    ], rows=[])

    def refresh() -> None:
        db = SessionLocal()
        try:
            items = crud.list_transactions(db, limit=200, description=search.value or None)
            rows_table.rows = [
                {"id": t.id, "date": str(t.transaction_date), "description": t.description, "amount": float(t.amount)}
                for t in items
            ]
            rows_table.update()
        finally:
            db.close()

    def add_dummy() -> None:
        db = SessionLocal()
        try:
            payload = {
                "transaction_date": "2024-01-01",
                "description": "Manual Transaction",
                "amount": Decimal("-1.00"),
                "currency": "USD",
                "transaction_type": "expense",
                "source_file": "manual",
                "fingerprint_hash": "",
            }
            payload["fingerprint_hash"] = build_fingerprint(payload)
            crud.create_transaction(db, TransactionCreate(**payload))
            ui.notify("Transaction created")
            refresh()
        finally:
            db.close()

    ui.button("Search", on_click=refresh)
    ui.button("Add Sample Transaction", on_click=add_dummy)
    refresh()
