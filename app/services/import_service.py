"""Import service that orchestrates statement pipeline integration."""

import json
import logging
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app import crud, models, schemas
from statement_import.pipeline import StatementImportPipeline

logger = logging.getLogger(__name__)


class ImportService:
    """Facade for initiating parser pipeline and returning report payloads."""

    def __init__(self) -> None:
        self.pipeline = StatementImportPipeline()
        self.preview_store: dict[str, dict] = {}

    def preview_import(self, file_path: str, password: str | None = None) -> dict:
        logger.info("Generating preview for %s", file_path)
        report = self.pipeline.run(Path(file_path), password=password, preview_only=True)
        preview_id = str(uuid.uuid4())
        self.preview_store[preview_id] = report
        report["preview_id"] = preview_id
        return report

    def execute_import(self, preview_id: str, db: Session) -> dict:
        preview = self.preview_store.get(preview_id)
        if not preview:
            raise ValueError("Preview ID not found. Generate preview first.")

        inserted = 0
        skipped = 0
        for row in preview["normalized_transactions"]:
            if row.get("is_duplicate") or crud.fingerprint_exists(db, row["fingerprint_hash"]):
                skipped += 1
                continue

            tx = schemas.TransactionCreate(**row)
            crud.create_transaction(db, tx)
            inserted += 1

        history = crud.create_statement_import(
            db,
            {
                "source_file": preview["source_file"],
                "bank_name": preview["classification"].get("bank_name"),
                "status": "success",
                "total_rows_detected": preview["detected_transactions"],
                "total_rows_imported": inserted,
                "total_rows_skipped": skipped,
                "report_json": json.dumps(
                    {
                        "selected_parser": preview.get("selected_parser"),
                        "warnings": preview.get("warnings", []),
                        "errors": preview.get("errors", []),
                    }
                ),
            },
        )

        for tx in db.query(models.Transaction).filter(models.Transaction.source_file == preview["source_file"]).all():
            if tx.statement_id == 0:
                tx.statement_id = history.id
        db.commit()

        return {"history_id": history.id, "inserted": inserted, "skipped": skipped}

    def list_history(self, db: Session) -> list[models.StatementImport]:
        return crud.list_import_history(db)
