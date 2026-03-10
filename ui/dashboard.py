"""Dashboard page for FinFlow."""

from sqlalchemy import func, select

from app import models
from app.database import SessionLocal
from ui.charts import render_category_spend, render_income_vs_expense
from nicegui import ui


def render_dashboard() -> None:
    ui.label("FinFlow Dashboard").classes("text-h4")
    db = SessionLocal()
    try:
        month_rows = db.execute(
            select(
                func.strftime("%Y-%m", models.Transaction.transaction_date),
                func.sum(models.Transaction.amount),
            ).group_by(func.strftime("%Y-%m", models.Transaction.transaction_date))
        ).all()

        labels = [r[0] for r in month_rows] or ["N/A"]
        income = [float(r[1]) if float(r[1] or 0) > 0 else 0 for r in month_rows] or [0]
        expense = [abs(float(r[1])) if float(r[1] or 0) < 0 else 0 for r in month_rows] or [0]

        with ui.card().classes("w-full"):
            ui.label("Monthly Income vs Expenses")
            render_income_vs_expense(labels, income, expense)

        cat_rows = db.execute(
            select(models.Category.name, func.sum(models.Transaction.amount))
            .join(models.Transaction, models.Transaction.category_id == models.Category.id)
            .group_by(models.Category.name)
        ).all()

        with ui.card().classes("w-full"):
            ui.label("Spending by Category")
            render_category_spend([r[0] for r in cat_rows] or ["No Data"], [abs(float(r[1] or 0)) for r in cat_rows] or [1])

        recent = db.scalars(select(models.Transaction).order_by(models.Transaction.transaction_date.desc()).limit(10)).all()
        with ui.card().classes("w-full"):
            ui.label("Recent Transactions")
            ui.table(
                columns=[
                    {"name": "date", "label": "Date", "field": "date"},
                    {"name": "description", "label": "Description", "field": "description"},
                    {"name": "amount", "label": "Amount", "field": "amount"},
                ],
                rows=[
                    {"date": str(t.transaction_date), "description": t.description, "amount": float(t.amount)}
                    for t in recent
                ],
            )
    finally:
        db.close()
