"""Import history page skeleton."""

from nicegui import ui


def render_import_history_page() -> None:
    ui.label("Import History").classes("text-h4")
    ui.table(columns=[
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "source", "label": "Source File", "field": "source"},
        {"name": "status", "label": "Status", "field": "status"},
        {"name": "imported", "label": "Imported", "field": "imported"},
    ], rows=[])
