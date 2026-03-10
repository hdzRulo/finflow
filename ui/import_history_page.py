"""Import history page."""

from nicegui import ui

from app.database import SessionLocal
from app.services.import_service import ImportService

service = ImportService()


def render_import_history_page() -> None:
    ui.label("Import History").classes("text-h4")
    table = ui.table(columns=[
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "source", "label": "Source File", "field": "source"},
        {"name": "status", "label": "Status", "field": "status"},
        {"name": "found", "label": "Found", "field": "found"},
        {"name": "imported", "label": "Imported", "field": "imported"},
        {"name": "skipped", "label": "Skipped", "field": "skipped"},
    ], rows=[])

    db = SessionLocal()
    try:
        rows = service.list_history(db)
        table.rows = [
            {
                "id": r.id,
                "source": r.source_file,
                "status": r.status,
                "found": r.total_rows_detected,
                "imported": r.total_rows_imported,
                "skipped": r.total_rows_skipped,
            }
            for r in rows
        ]
        table.update()
    finally:
        db.close()
