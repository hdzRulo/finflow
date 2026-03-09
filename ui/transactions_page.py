"""Transactions page skeleton."""

from nicegui import ui


def render_transactions_page() -> None:
    ui.label("Transactions").classes("text-h4")
    ui.input("Search description")
    ui.select(options=["all", "income", "expense"], value="all", label="Type")
    ui.table(columns=[
        {"name": "date", "label": "Date", "field": "date"},
        {"name": "description", "label": "Description", "field": "description"},
        {"name": "amount", "label": "Amount", "field": "amount"},
    ], rows=[])
