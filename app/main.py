"""FastAPI + NiceGUI entrypoint for FinFlow."""

import logging

from fastapi import FastAPI
from nicegui import ui

from app.api import categories, imports, transactions
from app.config import settings
from app.database import Base, engine
from ui.dashboard import render_dashboard
from ui.import_history_page import render_import_history_page
from ui.import_page import render_import_page
from ui.transactions_page import render_transactions_page

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name)

app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(imports.router)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize DB schema on startup for scaffold usability."""
    Base.metadata.create_all(bind=engine)


@ui.page("/")
def dashboard_page() -> None:
    render_dashboard()


@ui.page("/transactions")
def transactions_page() -> None:
    render_transactions_page()


@ui.page("/import")
def import_page() -> None:
    render_import_page()


@ui.page("/import-history")
def history_page() -> None:
    render_import_history_page()
