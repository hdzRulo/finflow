"""Plotly chart helpers for NiceGUI pages."""

import plotly.graph_objects as go
from nicegui import ui


def render_income_vs_expense(labels: list[str], income: list[float], expense: list[float]) -> None:
    fig = go.Figure(data=[go.Bar(name="Income", x=labels, y=income), go.Bar(name="Expense", x=labels, y=expense)])
    fig.update_layout(barmode="group", height=300, margin=dict(l=20, r=20, t=20, b=20))
    ui.plotly(fig)


def render_category_spend(labels: list[str], values: list[float]) -> None:
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
    ui.plotly(fig)
