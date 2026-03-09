"""Plotly chart helpers for NiceGUI pages."""

import plotly.graph_objects as go
from nicegui import ui


def render_monthly_summary_chart() -> None:
    fig = go.Figure(
        data=[
            go.Bar(name="Income", x=["Jan", "Feb", "Mar"], y=[0, 0, 0]),
            go.Bar(name="Expense", x=["Jan", "Feb", "Mar"], y=[0, 0, 0]),
        ]
    )
    fig.update_layout(barmode="group", height=300, margin=dict(l=20, r=20, t=20, b=20))
    ui.plotly(fig)
