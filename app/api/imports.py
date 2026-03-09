"""Import API endpoints for statement uploads and history."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["imports"])
service = ImportService()


@router.post("/preview")
def preview_import(payload: schemas.StatementImportCreate):
    """Preview parsing results before database persistence."""
    return service.preview_import(payload.source_file)


@router.post("/run")
def run_import(payload: schemas.StatementImportCreate, db: Session = Depends(get_db)):
    """Execute import and create history record placeholder."""
    report = service.execute_import(payload.source_file)
    history = crud.create_statement_import(db, payload)
    return {"history_id": history.id, "report": report}
