"""Statement import preview page."""

from pathlib import Path

from nicegui import ui

from app.database import SessionLocal
from app.services.import_service import ImportService

service = ImportService()


def render_import_page() -> None:
    ui.label("Import Statement").classes("text-h4")
    password = ui.input("Optional PDF password", password=True, password_toggle_button=True)
    selected_path = {"value": ""}
    preview_id = {"value": ""}

    def on_upload(e):
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / e.name
        file_path.write_bytes(e.content.read())
        selected_path["value"] = str(file_path)
        ui.notify(f"Uploaded {e.name}")

    ui.upload(on_upload=on_upload, auto_upload=True)
    preview_table = ui.table(columns=[
        {"name": "date", "label": "Date", "field": "date"},
        {"name": "description", "label": "Description", "field": "description"},
        {"name": "amount", "label": "Amount", "field": "amount"},
        {"name": "dup", "label": "Duplicate", "field": "dup"},
    ], rows=[])

    parser_label = ui.label("Parser: N/A")

    def do_preview() -> None:
        if not selected_path["value"]:
            ui.notify("Upload a PDF first", color="negative")
            return
        report = service.preview_import(selected_path["value"], password=password.value or None)
        preview_id["value"] = report["preview_id"]
        parser_label.set_text(f"Parser: {report['selected_parser']}")
        preview_table.rows = [
            {
                "date": str(r.get("transaction_date")),
                "description": r.get("description"),
                "amount": float(r.get("amount", 0)),
                "dup": r.get("is_duplicate"),
            }
            for r in report["normalized_transactions"]
        ]
        preview_table.update()
        ui.notify(f"Preview ready ({report['detected_transactions']} rows)")

    def do_confirm() -> None:
        if not preview_id["value"]:
            ui.notify("Run preview first", color="negative")
            return
        db = SessionLocal()
        try:
            result = service.execute_import(preview_id["value"], db)
            ui.notify(f"Imported {result['inserted']} / skipped {result['skipped']}")
        finally:
            db.close()

    ui.button("Preview Import", on_click=do_preview)
    ui.button("Confirm Import", on_click=do_confirm, color="primary")
