"""Dashboard page skeleton for FinFlow."""

from nicegui import ui

from ui.charts import render_monthly_summary_chart


def render_dashboard() -> None:
    ui.label("FinFlow Dashboard").classes("text-h4")
    ui.row().classes("w-full gap-4")
    with ui.card().classes("w-full"):
        ui.label("Monthly Summary (Placeholder)")
        render_monthly_summary_chart()
